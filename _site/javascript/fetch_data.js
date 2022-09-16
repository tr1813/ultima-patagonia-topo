const Http = new XMLHttpRequest();
const url='https://github.com/tr1813/ultima-patagonia-topo/releases/download/latest/cadastre.js';
Http.open("GET", url);
Http.send();

Http.onreadystatechange = (e) => {
  console.log(Http.responseText)
}
