d3.json("manga_data.json").then(rawDictionary => {
    
    // 1. Flatten the dictionary into an array
    const mangaData = Object.values(rawDictionary);
    
    const width = 800;
    const height = 600;

    const svg = d3.select("#chart-container")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    const defs = svg.append("defs");

    // 2. Updated to use d.slug and d.coverUrl
    mangaData.forEach(d => {
        defs.append("pattern")
            .attr("id", `pattern-${d.slug}`)
            .attr("width", 1)
            .attr("height", 1)
            .attr("patternContentUnits", "objectBoundingBox")
            .append("image")
            .attr("href", d.coverUrl)
            .attr("width", 1)
            .attr("height", 1)
            .attr("preserveAspectRatio", "xMidYMid slice");
    });

    // 3. Updated to use d.read_chapter_count
    const radiusScale = d3.scaleSqrt()
        .domain([0, d3.max(mangaData, d => d.read_chapter_count || 10)])
        .range([35, 75]); 

    // 4. Updated collision radius to use read_chapter_count
    const simulation = d3.forceSimulation(mangaData)
        .force("charge", d3.forceManyBody().strength(-15))
        .force("x", d3.forceX(width / 2).strength(0.08))
        .force("y", d3.forceY(height / 2).strength(0.08))
        .force("collide", d3.forceCollide().radius(d => radiusScale(d.read_chapter_count || 10) + 4).iterations(2));

    const node = svg.append("g")
        .selectAll("circle")
        .data(mangaData)
        .join("circle")
        .attr("class", "node")
        .attr("r", d => radiusScale(d.read_chapter_count || 10))
        .attr("fill", d => `url(#pattern-${d.slug})`)
        .style("filter", d => d.caught_up ? "grayscale(100%)" : "none")
        .call(drag(simulation))
        
        // ADD THIS NEW CLICK EVENT LISTENER
        .on("click", (event, d) => {
            
            // 1. The Safety Valve: Ignore the click if the user was actually dragging
            if (event.defaultPrevented) return; 
            
            // 2. The Link Logic
            if (d.url) {
                // If you added a 'url' to your JSON, open it in a new tab
                window.open(d.url, "_blank");
            } else {
                // Alternatively, construct the URL dynamically using the slug!
                // For example, routing them to a custom reader or proxy
                const dynamicUrl = `https://weebcentral.com/series/${d.slug}`;
                window.open(dynamicUrl, "_blank");
            }
            
        });

    node.append("title")
        .text(d => `${d.title}`);

    simulation.on("tick", () => {
        node
            .attr("cx", d => {
                const r = radiusScale(d.read_chapter_count || 10); 
                return d.x = Math.max(r, Math.min(width - r, d.x || 0)); 
            })
            .attr("cy", d => {
                const r = radiusScale(d.read_chapter_count || 10);
                return d.y = Math.max(r, Math.min(height - r, d.y || 0));
            });
    });

    function drag(simulation) {
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x; d.fy = d.y;
        }
        function dragged(event, d) {
            d.fx = event.x; d.fy = event.y;
        }
        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null; d.fy = null;
        }
        return d3.drag().on("start", dragstarted).on("drag", dragged).on("end", dragended);
    }

}).catch(error => {
    console.error("Error loading manga_data.json:", error);
});

async function fetchData(query) {
    try {
        const encodedQuery = encodeURIComponent(query);
        
        // A relative path will automatically use https://duckdns.org
        const response = await fetch(`/api/search?text=${encodedQuery}`);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Server error');
        }
        
        const data = await response.json(); 
        const mangaID = data.mangaID;
        
        console.log(`Success! Python extracted the Manga ID: ${mangaID}`);
        
        // Move to your layout/chart logic
        renderMangaData(mangaID);
        return mangaID;

    } catch (error) {
        console.error('Frontend Error:', error.message);
    }  
}



// Identify HTML elements (Added the form element)
const searchForm = document.getElementById('searchForm');
const searchBar = document.getElementById('searchBar');

// Handle the search event safely
function handleSearch(event) {
    // 1. Prevent the form from reloading the page (fixes Enter key bug)
    event.preventDefault(); 

    // 2. Extract the text that is in the search bar
    const searchText = searchBar.value; 
    
    // 3. Run your fetch function
    fetchData(searchText); 
}

// Attach the listener to the FORM submit event, not the button click
searchForm.addEventListener('submit', handleSearch);