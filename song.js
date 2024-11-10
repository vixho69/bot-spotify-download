import fs from 'fs';
import fetch from 'node-fetch';



// Get URL from arguments
const url = process.argv[2];

if (!url) {
    console.error("URL required.");
    process.exit(1);
}

const headers = {
    "Host": "api.spotifydown.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.3; rv:129.0) Gecko/20000101 Firefox/129.0",
    "Accept": "*/*",
    "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://spotifydown.com/",
    "Origin": "https://spotifydown.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Sec-Ch-Ua-Platform": '"macOS"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Priority": "u=0",
    "Te": "trailers"
};

fetch(url, { method: 'GET', headers: headers })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        // Verify that the data structure is as expected
        if (data.metadata) {
            const extractedData = {
                id: data.metadata.id,
                artists: data.metadata.artists,
                title: data.metadata.title,
                album: data.metadata.album,
                cover: data.metadata.cover,
                releaseDate: data.metadata.releaseDate,
                link: data.link
            };

            // Save data to a JSON file
            fs.writeFileSync('data.json', JSON.stringify(extractedData, null, 2));
            console.log("Data saved in data.json");
        } else {
            console.error("The response does not contain the expected data.");
        }
    })
    .catch(error => {
        console.error("Request error:", error);
    });
