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
                
        return mangaID;
    } catch (error) {
        console.error('Frontend Error:', error.message);
    }  
}

// Identify HTML elements
const searchForm = document.getElementById('searchForm');
const searchBar = document.getElementById('searchBar');

// 1. Add 'async' to the function so you can use 'await' inside it
async function handleSearch(event) {
    event.preventDefault(); 
    const searchText = searchBar.value; 

    try {
        const mangaID = await fetchData(searchText); 
        
        if (mangaID) {
            // This will NEVER be blocked by a mobile browser
            window.location.href = `https://cubari.moe/read/weebcentral/${mangaID}/`;
        } else {
            alert('Manga not found. Please try another search.');
        }
    } catch (error) {
        console.error('Search Handler Error:', error);
    }
}

// Attach the listener to the FORM submit event
searchForm.addEventListener('submit', handleSearch);

alert("JavaScript loaded successfully!");