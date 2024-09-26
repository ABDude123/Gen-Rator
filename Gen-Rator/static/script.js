function generateCode() {
    fetch('/generate')
        .then(response => response.json())
        .then(data => {
            document.querySelector("#code span").innerText = data.code;
            document.querySelector("#status span").innerText = data.status + " (API Status: " + data.api_status + ")";
        });
}