const boton = document.getElementById("menu-btn");

const sidebar = document.getElementById("sidebar");

boton.addEventListener("click", ()=>{

    sidebar.classList.toggle("active");

});