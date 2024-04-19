import React from "react";
import "./Navbar.css";
import { Col, Nav, Row } from "react-bootstrap";


const Navbar = (props) => {
const {handleUploadPdf}=props

  return (
    <div className="border-shadow header col-md-12 py-4">
      <div className="responsive-width px-4">
        <Row className="responsive-md resposive-lg m-0 p-0">
          <Col className="cursor-pointer d-flex align-items-center p-0">
            <span id="heading">Real-time PDF Summary</span>

          </Col>
          {/* <Col xs sm={6} md={6} lg={6} className="text-overflow align-self-center p-0 nav-content">
            <Nav className="display-flex justify-content-between align-items-center">
              <div>
                <button onClick={handleUploadPdf} id="contact-btn">Upload PDF</button>
              </div>
            </Nav>
          </Col> */}
        </Row>
      </div>
    </div>
  )
};

export default Navbar;
