document.addEventListener('DOMContentLoaded', function (){
const progressbar = document.querySelector("#barr");
const photo = document.querySelector("#photo");
const dot = document.querySelector('#dott');
const innerBar = document.querySelector(".innerbar");
const innerContents = document.querySelectorAll(".inner-content");
const bar = document.querySelector('.bar');
const image = document.querySelector("#img");
const blockdiv = document.querySelector('.createplaylists');
const c = document.querySelector('.e');
const x = document.querySelector('.fa-xmark');
const editbutton = document.querySelector('.editbutton');
const detailsImg = document.querySelector('.details-img');
const fileInput = document.getElementById('fileInput');
const icon = document.querySelector('.fa-music');
const createP = document.querySelectorAll('.create-playlist');
const saveButton = document.getElementById('saveButton');
const chosenImg = document.getElementById('chosenImg');
const playlistTitle = document.getElementById('playlistTitle');
const playlistnameInput = document.getElementById('playlistname');
const innerclick = document.querySelector('.innerclick');
const innerclick2 = document.querySelector('.innerclick2');
const inneroption = document.querySelector('.inner-option');
const innerA = document.querySelectorAll('.inner-option > a');
const optionBottomLeft = document.querySelector('.option-bottom-left');
const info = document.querySelector('.info');

let selectedImage = null;

info.addEventListener("click", () => {
    window.location.href= "/playlists";
});


let translateX = -80;


c.addEventListener("click", () => {
    blockdiv.classList.add("active");
    console.log("clicked c");
});

x.addEventListener("click", () => {
    blockdiv.classList.remove("active");
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        blockdiv.classList.remove("active");
    }
});

progressbar.addEventListener('mouseover', () => {
    dot.style.width = "12px";
    innerBar.style.background = "#1ed660";
});
progressbar.addEventListener('mouseout', () => {
    dot.style.width = "10px";
    innerBar.style.background = "";
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
    const lastCardObserver = new IntersectionObserver(
        entries => {
            const lastCard = entries[0]
            if(lastCard.isIntersecting){
                innerclick.style.scale = "0 1";
                optionBottomLeft.classList.add('inactive');
            }else{
                innerclick.style.scale = "1 1";
                optionBottomLeft.classList.remove('inactive');
            }
        },
        {
            threshold: 1,
        }
    );

    saveButton.addEventListener('click', () => {
        const playlistName = playlistnameInput.value;

        if (selectedImage && playlistName) {
            if (selectedImage) {
                chosenImg.src = selectedImage;
            }

            if (playlistName) {
                playlistTitle.textContent = playlistName;
            }
            createP.forEach(create => {
                create.style.display = "none";
            });

            innerContents.forEach(innerContent => {
                innerContent.style.display = "flex";
            });

            blockdiv.classList.remove("active");
        } else {
            window.alert('Please choose an image or enter a playlist name.'); 
        }
       
    });
    const firstCardObserver = new IntersectionObserver(
        entries => {
            const firstCard = entries[0]
            if(firstCard.isIntersecting){
                innerclick2.style.scale = "0 1";
                optionBottomLeft.classList.remove('active');
                translateX = 0;
            }else{
                innerclick2.style.scale = "1 1";
            }
        },
        {
            threshold: 1,
        }
    );
    

    lastCardObserver.observe(document.querySelector(".inner-option > a:last-child"))
    firstCardObserver.observe(document.querySelector(".inner-option > a:first-child"))

    
    innerclick.addEventListener("click", () => {
        console.log(translateX);
        translateX-=80;
        if(translateX === 0){
            inneroption.style.transform = `translateX(${translateX}px)`;
            optionBottomLeft.classList.remove('active');
            innerclick2.style.opacity = "0";
        }else{
            innerclick2.style.opacity = "1";
            optionBottomLeft.classList.add('active');
            inneroption.style.transform = `translateX(${translateX}px)`;
        }
        
    });

    innerclick2.addEventListener("click", () =>{ 
        console.log(translateX);  
        translateX+=80;
        inneroption.style.transform = `translateX(${translateX}px)`;
    });


       

        detailsImg.addEventListener('click', () => {
            fileInput.click();
        });

        fileInput.addEventListener('change', (event) => {
            const files = event.target.files;
            if (files.length > 0) {
                const file = files[0];
                const reader = new FileReader();

                reader.onload = function(e) {
                    detailsImg.style.backgroundImage = `url(${e.target.result})`;
                    selectedImage = e.target.result;
                    if (icon) {
                        icon.remove(); 
                    }
                }

                reader.readAsDataURL(file);
            }
        });

       


    image.addEventListener("mouseover", () => {
        image.style.filter = "brightness(0.5)";
        photo.style.opacity = "1";
    });
    image.addEventListener("mouseout", () => {
        image.style.filter = "";
        photo.style.opacity = "0";
    });

    editbutton.addEventListener("click", () => {
        blockdiv.classList.remove("active");
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
});


