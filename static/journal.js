window.onload = function(){

}

function submit_journal()
{
    const textVal = document.getElementById("journalTxt").value
    fetch('/journalling',{
        method:"POST",
        body: JSON.stringify({
            content: textVal,
            date: getTodayDate(),
          }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
          }
    })
}

function getTodayDate() {
    const today = new Date();

    const year = today.getFullYear();
    const month = (today.getMonth() + 1).toString().padStart(2, '0'); // Months are 0-indexed, so we add 1
    const day = today.getDate().toString().padStart(2, '0'); // Ensure the day is 2 digits

    return `${year}-${month}-${day}`;
}

function loadHome()
{
    window.location.href="/"
}

function loadDash()
{
    window.location.href="/dashboard"
}

function loadAbout()
{
    window.location.href="/aboutus"
}