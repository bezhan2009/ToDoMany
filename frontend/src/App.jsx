import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  fetchDataStart,
  fetchDataSuccess,
  fetchDataFailure,
} from "./redux/slices/environment";
import API from "./getAPI";
import Home from "./pages/home/Home";
import Header from "./components/Header";
import "./App.css";

function App() {
  const [menuOpen, setMenuOpen] = useState(false);
  const dispatch = useDispatch();
  const data = useSelector((state) => state.data);

  useEffect(() => {
    dispatch(fetchDataStart());
    // Замість виклику API.get() тепер використовуємо Redux action для запиту даних
    API.get()
      .then((response) => {
        dispatch(fetchDataSuccess(response));
      })
      .catch((error) => {
        dispatch(fetchDataFailure(error.message));
      });
  }, [dispatch]);

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
        {/* Використовуйте дані зі стору Redux */}
        <Home data={data} />
      </div>
    </>
  );
}

export default App;
