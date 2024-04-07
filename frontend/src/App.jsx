import { useState, useEffect } from "react";
import Home from "./pages/home/Home";
import Header from "./components/Header";
import response from "./PostService";
import "./App.css";

function App() {
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    response.get();
  }, []);

  const handleChangeHeaderToggleSwitch = () => {
    setMenuOpen((prevState) => !prevState);
    console.log(menuOpen);
  };

  return (
    <>
      <Header
        menuOpen={menuOpen}
        onChangeHeaderToggleSwitch={handleChangeHeaderToggleSwitch}
        nameOfPage={"Главная страница"}
      />
      <div className={`content-container ${menuOpen ? "menu-open" : ""}`}>
        <Home />
      </div>
    </>
  );
}

export default App;
