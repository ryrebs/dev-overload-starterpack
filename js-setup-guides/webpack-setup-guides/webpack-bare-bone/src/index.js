import _ from 'lodash';
import './style.css'

function component() {
    let element = document.createElement('div');
    var btn = document.createElement('button');
 
    element.innerHTML = _.join(['Hello', 'webpack'], ' ');
    
    btn.innerHTML = 'Click me and check the console!';
    element.appendChild(btn);


    return element;
  }
  
  document.body.appendChild(component());