async function fetchRepositories() {
    const username = await getGithubUsernameFromDatabase();
    
    if (!username) {
        document.getElementById('message').innerHTML = 
            'GitHub username not found. Please click the <strong>Profile</strong> button to set it.';
        return;
    }

    document.getElementById('message').textContent = `Fetching repositories for ${username}...`;

    try {
        const response = await fetch(`https://api.github.com/users/${username}/repos`);
        
        if (!response.ok) {
            throw new Error('Error fetching repositories');
        }

        const repos = await response.json();
        const repoList = document.getElementById('repo-list');
        repoList.innerHTML = '';

        if (repos.length === 0) {
            repoList.innerHTML = '<p>No repositories found.</p>';
            return;
        }

        repos.forEach(repo => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<a href="${repo.html_url}" target="_blank">${repo.name}</a>`;
            repoList.appendChild(listItem);
        });
    } catch (error) {
        document.getElementById('message').textContent = 'Failed to fetch repositories. Please try again later.';
    }
}

async function getGithubUsernameFromDatabase() {
    try {
        const response = await fetch('/get-github-username'); // Endpoint to fetch GitHub username
        
        if (!response.ok) {
            throw new Error('Error fetching username from database');
        }

        const data = await response.json();
        return data.username || null;
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}