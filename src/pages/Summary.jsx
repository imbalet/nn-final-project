import { useState } from 'react'
import './Summary.css'
import '../components/Header.jsx'
import Header from '../components/Header.jsx'
import '../components/TextArea.jsx'
import Footer from '../components/Footer.jsx'
import TextAreaWithButton from '../components/TextAreaWithButton.jsx'

function Summary() {
  return (
    <div>
    <Header />
    <div className='paragraph'>
    <h2>Тут будет Суммаризация</h2> 
      <TextAreaWithButton />
      </div>
    <Footer/>
    </div>
  )
}

export default Summary
