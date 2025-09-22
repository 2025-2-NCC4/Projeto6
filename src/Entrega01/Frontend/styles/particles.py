import streamlit as st
import streamlit.components.v1 as components

def inject_particles():
    particles_background = """
    <style>
        #particles-js {
            position: fixed;
            width: 100%;
            height: 100%;
            z-index: -1;
            top: 0;
            left: 0;
        }
    </style>
    <div id=\"particles-js\"></div>
    <script src=\"https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js\"></script>
    <script>
    particlesJS(\"particles-js\", {
        \"particles\": {
            \"number\": {
                \"value\": 80,
                \"density\": {
                    \"enable\": true,
                    \"value_area\": 800
                }
            },
            \"color\": {
                \"value\": \"#fff\"
            },
            \"shape\": {
                \"type\": \"circle\"
            },
            \"opacity\": {
                \"value\": 0.5,
                \"random\": false
            },
            \"size\": {
                \"value\": 3,
                \"random\": true
            },
            \"line_linked\": {
                \"enable\": true,
                \"distance\": 150,
                \"color\": \"#007031\",
                \"opacity\": 1,
                \"width\": 1
            },
            \"move\": {
                \"enable\": true,
                \"speed\": 1,
                \"direction\": \"none\",
                \"out_mode\": \"out\"
            }
        },
        \"interactivity\": {
            \"events\": {
                \"onhover\": {
                    \"enable\": true,
                    \"mode\": \"repulse\"
                },
                \"onclick\": {
                    \"enable\": true,
                    \"mode\": \"push\"
                }
            },
            \"modes\": {
                \"repulse\": {
                    \"distance\": 100
                },
                \"push\": {
                    \"particles_nb\": 4
                }
            }
        },
        \"retina_detect\": true
    });
    </script>
    """
    components.html(particles_background, height=200)