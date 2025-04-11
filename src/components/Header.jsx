import './Header.css'
import logo from '/src/assets/logo.svg'

export default function Header(){
    return(
        <header className="header">
            <h1>Summary AI</h1>
            <div className="logo" >
            <img src={logo}/>
            </div>
        </header>
    )
}