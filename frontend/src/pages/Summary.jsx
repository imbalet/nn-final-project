import { useState } from 'react'
import './Summary.css'
import '../components/Header.jsx'
import Header from '../components/Header.jsx'
import '../components/TextArea.jsx'
import Footer from '../components/Footer.jsx'
import TextAreaWithButton from '../components/TextAreaWithButton.jsx'
import TextArea from '../components/TextArea.jsx'

function Summary() {
  return (
    <div>
    <Header />
    <div className='paragraph'>

      <TextAreaWithButton rows='1'/>
      <TextArea  />
      </div>
    <Footer/>
    </div>
  )
}

export default Summary
