import React from "react";
import { Col, Row } from "react-bootstrap";
import "./Footer.css";
import { useLocation } from "react-router-dom";

const Footer = () => {

  const location = useLocation();

  return (
    <div className="footer px-5">
      <div className="info-content responsive-width">
        <div className="p-0 m-0 py-3" style={{ display: 'flex', justifyContent: 'space-between' }}>
          <div className="contacts ">
            <div id="email-contact" className="">
              <a href="mailto:rpranjan11@gmail.com" className="email text-hover">
                <i className="bi bi-envelope-fill"></i>
                rpranjan11@gmail.com
              </a>
            </div>
            
            <div className="social-app-icons pt-2">

              <a
                href="https://www.linkedin.com/in/rpranjan11/"
                target="_blank"
                rel="noopener noreferrer"
              >

                <div className={`icon linkedin`}>
                  <div className="tooltip">
                    LinkedIn
                  </div>
                  <span>
                    <i className="fa-brands fa-linkedin-in"></i>
                  </span>
                </div>
              </a>

              <a
                href="https://github.com/rpranjan11"
                target="_blank"
                rel="noopener noreferrer"
              >

                <div className={`icon linkedin`}>
                  <div className="tooltip">
                    GitHub
                  </div>
                  <span>
                    <i className="fa-brands fa-github"></i>
                  </span>
                </div>
              </a>
            </div>
          </div>

          <div style={{display:'flex',alignItems:'flex-end'}}>
              <span className="copy-right">
                Designed & Developed by Ram Pratap Ranjan
              </span>
            </div>

          <div className="services ">
            <span id="heading" className="">
              <a href="https://github.com/rpranjan11/tampere_llm_assignment">
                <button>GitHub Project Link</button>
              </a>
            </span>
          </div>

        </div>
      </div>
    </div>
  )

};

export default Footer;
