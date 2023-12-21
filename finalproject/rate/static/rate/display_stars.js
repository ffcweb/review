var elements= document.getElementsByClassName("review_rate_stars")
for(let e of elements){
    var numberOfStars= Math.round(Number(e.innerHTML));
    e.innerHTML ="⭐".repeat(numberOfStars)+"✩".repeat(5-numberOfStars);
}