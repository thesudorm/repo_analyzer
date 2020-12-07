const { request } = require("@octokit/request");

const requestWithAuth = request.defaults({
    headers: {
        authorization: "token 5f012ae5825a8b9139e9e013ac709fac3d0dc2a7",
    },
});

for(var i = 0; i < 10; i++){
    requestWithAuth("GET /search/repositories", {
        q: 'stars:>=5000 language:c++ language:java language:c language:csharp',
        sort: 'stars',
        order: 'desc',
        per_page: 100
    }).then((results) => {
        //console.log(results)
        for (var result of results.data.items) {
            //console.log(result)
            //console.log(result["stars"])
            //console.log(result["stargazers_count"])
            console.log(result.full_name + "," + result.git_url + "," + result.stargazers_count + "," + result.language)
        }
    })
}
