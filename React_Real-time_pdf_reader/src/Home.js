import React, { useState ,useRef,useEffect} from "react";
import { Row, Col } from "react-bootstrap";
import "./Home.css"
import Navbar from "./Navbar/Navbar";
import Footer from "./footer/Footer";
import pdfToText from 'react-pdftotext'
import axios from "axios";



export const Home = () => {
    const email = "email"
    const [file, setFile] = useState("")
    const [fileName, setFileName] = useState("")

    const textRef = useRef(null);
    const lastAnswerRef = useRef(null);
    const formRef = useRef(null);


    const [fileText, setFileText] = useState("")

    const [que1, setQue1] = useState("")
    const [que2, setQue2] = useState("")

    const [queArr1, setQueArr1] = useState([])
    const [ansArr1, setAnsArr1] = useState([])
    const [text1, setText1] = useState("")


    const [queArr2, setQueArr2] = useState([])
    const [ansArr2, setAnsArr2] = useState([])
    const [text2, setText2] = useState("")

    const scrollToBottom = () => {
        if (textRef.current) {
            textRef.current.scrollIntoView({ behavior: 'smooth', block: 'end' });
        }
    }
    useEffect(() => {
        scrollToBottom(); // Scroll to bottom on initial render
    }, []); 

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        const fileName = selectedFile.name;
        setFileName(fileName)
        setFile(selectedFile);

        if (selectedFile) {
            pdfToText(selectedFile)
                .then(text => {
                    setFileText(text)
                })
                .catch(error => console.error("Failed to extract text from pdf"))
        }
    };

    const handleUploadPdf = () => {
        const formData = new FormData();
        formData.append('pdf', file); 
        
        axios.post('http://localhost:8000/loadpdf', formData)
            .then(response => {
                console.log(response.data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    };


    const handleQuestions1 = (text) => {
        setQueArr1((prev) => [...prev, text])
        // model = "openAPI"
        const url = `http://0.0.0.0:8000/getsummary1/${text}`;

        axios.get(url)
            .then(response => {
                setAnsArr1((prev) => [...prev, response.data.chatgptresponse])
                scrollToBottom(); // Scroll to bottom after adding question

                
            })
            .catch(error => {
                console.error('Error:', error);
            });

        setQue1("")

    }

    const handleQuestions2 = (text) => {
        setQueArr2((prev) => [...prev, text])
        // model = "ollama"
        const url = `http://0.0.0.0:8000/getsummary2/${text}`;

        axios.get(url)
            .then(response => {
                console.log('Response:', response.data);
                setAnsArr2((prev) => [...prev, response.data.ollamaresponse])

            })
            .catch(error => {
                console.error('Error:', error);
            });

        setQue2("")
    }

    const onClickCross = () => {
        setFile("")
        setFileName("")
        setText1("")
        setText2("")
        formRef.current.reset();

    }


      
    return (
        <div className="home_container">
            <Navbar handleUploadPdf={handleUploadPdf} />
            <div className="home_content">
                <div className="body_content">
                    <div style={{ display: 'flex', padding: '20px', justifyContent: 'center' }}>
                        <div>
                            <form ref={formRef}>
                                <input type="file" accept="application/pdf" id="file_input"
                                    onChange={handleFileChange}
                                />
                            </form>
                            {fileName && <span style={{ maxWidth: '500px' }}>{fileName}</span>}
                        </div>

                        <div style={{display:'flex',flexDirection:'column'}}>
                            <button onClick={handleUploadPdf} id="contact-btn">Upload PDF</button>
                            {file && <button id="close-btn" onClick={onClickCross}><i className="bi bi-x-lg"></i></button>}
                        </div>
                    </div>
                   {text1 && <div style={{flexGrow:'1',display:'flex'}}>
                        <Row style={{width:'100%'}}>
                            <Col md={6} lg={6} className="px-3 pb-4">
                                <div className="card-content">
                                    <div className="text" id="text-area" ref={textRef}>
                                        {text1 && <span>{text1}</span>}
                                        {
                                            queArr1.map((item, idx) => {
                                                return (
                                                    ansArr1[idx] && <div key={idx} style={{ display: 'flex', flexDirection: 'column' }}>
                                                        <span id="questions">-{item} </span>
                                                        <span id={idx!==ansArr1.length-1?"answers":'latest'} >{ansArr1[idx]}</span>
                                                    </div>
                                                )
                                            })
                                        }
                                    </div>
                                    <div style={{ display: 'flex', alignItems: 'center' }}>
                                        <input className="input_text" type="text" value={que1} onChange={(e) => {
                                            setQue1(e.target.value)
                                        }}></input>
                                        <i style={{ fontSize: '25px', cursor: 'pointer' }} onClick={() => handleQuestions1(que1)} className="bi bi-box-arrow-in-up px-3"></i>
                                    </div>
                                </div>
                            </Col>
                            <Col md={6} lg={6} className="px-3 pb-4">
                                <div className="card-content">
                                    <div className="text">
                                        {text2 && <span>{text2}</span>}
                                        {
                                            queArr2.map((item, idx) => {
                                                return (
                                                    ansArr2[idx] && <div key={idx} style={{ display: 'flex', flexDirection: 'column' }}>
                                                        <span id="questions">{item} </span>
                                                        <span id="answers">{ansArr2[idx]} </span>
                                                    </div>
                                                )
                                            })
                                        }
                                    </div>
                                    <div style={{ display: 'flex', alignItems: 'center' }}>
                                        <input className="input_text" type="text" value={que2} onChange={(e) => {
                                            setQue2(e.target.value)
                                        }}></input>
                                        <i style={{ fontSize: '25px', cursor: 'pointer' }} onClick={() => handleQuestions2(que2)} className="bi bi-box-arrow-in-up px-3"></i>
                                    </div>
                                </div>

                            </Col>
                        </Row>
                    </div>}
                </div>
            </div>
            <Footer />
        </div>
    )
}