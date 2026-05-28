// Fetch the JSON file your Python script generated
fetch('manga_data.json')
    .then(response => response.json())
    .then(data => {
        const grid = document.getElementById('grid');

        // Force the dictionary to become an array of manga objects
        Object.values(data).forEach(manga => {
            const bubble = document.createElement('div');
            bubble.className = 'manga-bubble';
            
            const isRead = manga.caught_up;
                                
            // If isRead is false, apply grayscale. Otherwise, no extra class.
            const imageClass = isRead === true ? 'grayscale' : '';

            bubble.innerHTML = `
                <a href="https://cubari.moe/read/weebcentral/${manga.slug}/" target="_blank" style="text-decoration: none; color: inherit; display: block;">
                    <img src="${manga.coverUrl || 'https://via.placeholder.com/200x280?text=No+Cover'}" alt="Cover", class="${imageClass}">
                    <div class="manga-info">
                        <h3>${manga.title || 'Unknown Title'}</h3>
                    </div>
                </a>
            `;
            grid.appendChild(bubble);
        });
    })
    .catch(error => console.error('Error loading manga data:', error));

async function fetchData(query) {
    try {
        const response = await fetch(`https://weebcentral.com/search/data?author=&text=${query}&sort=Best%20Match&order=Descending&official=Any&anime=Any&adult=Any&display_mode=Full%20Display`)
        if (!response.ok) throw new Error ('Request failed');
        const htmlString = await response.text();
        console.log(htmlString);

        const parser = new DOMParser();
        const doc = parser.parseFromString(htmlString, 'text/html');

        const anchorTag = doc.querySelector('a');

        const url = firstAnchor.getAttribute('href')
        // https://weebcentral.com/series/01J76XYFPF0C74JMR2H1MTQ2MR/Look-Back

        const urlParts = url.split("/")
        // ['https:', '', 'weebcentral.com', 'series', '01J76XYFPF0C74JMR2H1MTQ2MR', 'Look-Back']

        const mangaID = urlParts[4]
        // "01J76XYFPF0C74JMR2H1MTQ2MR"

        console.log(`Success! The extracted Manga ID is: ${mangaID}`)
    } catch (error) {
        console.error('Error:', error);
        console.log("Could not find the manga link on this page.")
    }  
}

const searchBar = document.getElementById('searchBar');
const searchButton = document.getElementById('searchButton');

function handleSearch() {
    const currentText = searchBar.value; 
    fetchData(currentText); 
}

searchButton.addEventListener('click', handleSearch);