let isScrolling = false;

async function caruselScroll(leftOrRight){
    if (isScrolling) return;

    isScrolling = true;

    await new Promise(resolve => {
        item = document.getElementById( "carusel" );
    
        let scroll = null;

        if (window.innerWidth > 600){
            scroll = parseInt((window.innerWidth-248)/5) + 32;
        } 
        else {
            scroll = item.clientWidth;
        }

        item.scroll({
            // left: item.scrollLeft + 342,
            left: item.scrollLeft + (leftOrRight * scroll),
            top: 0,
            behavior: 'smooth'
        })
        setTimeout(resolve, 500);
    })

    isScrolling = false;
}

document.getElementById( "right-button" ).onclick = () => caruselScroll(1)
document.getElementById( "left-button" ).onclick = () => caruselScroll(-1)
document.getElementById( "carusel" ).addEventListener("wheel", (event) => {
    if (event.shiftKey){
        event.preventDefault();
    }
    
})