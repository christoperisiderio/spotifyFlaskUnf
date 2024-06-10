const progressbar = document.querySelector("#barr");
const photo = document.querySelector("#photo");
const dot = document.getElementById('dott');
const innerBar = document.querySelector(".innerbar");
innerContents = document.querySelectorAll(".inner-content");
const bar = document.querySelector('.bar');
const image = document.querySelector("#img");

document.addEventListener('DOMContentLoaded', function (){

    image.addEventListener("mouseover", () => {
        image.style.filter = "brightness(0.5)";
        photo.style.opacity = "1";
    });
    image.addEventListener("mouseout", () => {
        image.style.filter = "";
        photo.style.opacity = "0";
    });





    dot.addEventListener('mousedown', function(event) {
        event.preventDefault();
    
        const barRect = bar.getBoundingClientRect();
        const barWidth = barRect.width;
    
        function onMouseMove(e) {
            let newLeft = e.clientX - barRect.left;
    
            if (newLeft < 0) {
                newLeft = 0;
            } else if (newLeft > barWidth) {
                newLeft = barWidth;
            }
    
            const newWidthPercentage = (newLeft / barWidth) * 100;
            dot.style.left = `calc(${newWidthPercentage}% - 5px)`;
            if (newWidthPercentage > 1){
                document.querySelector('.innerbar').style.width = `${newWidthPercentage}%`;
            }else{
                document.querySelector('.innerbar').style.width = '1%';
            }
        }
    
        function onMouseUp() {
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
        }
    
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', onMouseUp);
    });



    progressbar.addEventListener('mouseover', () => {
        dot.style.width = "12px";
        innerBar.style.background = "#1ed660";
    });
    progressbar.addEventListener('mouseout', () => {
        dot.style.width = "10px";
        innerBar.style.background = "";
    });
    
    innerContents.forEach(innerContent => {
        let count = 1;
        innerContent.addEventListener("click", () => {
            if (count%2 == 0){
                innerContent.style.color = "rgb(205, 211, 214)";
                console.log("success");
            }else{
                innerContent.style.color = "#1ed660";
            }
            count = count + 1;
        });
    });

    dot.addEventListener("hold", () =>{
        console.log("ge");
    });
});


