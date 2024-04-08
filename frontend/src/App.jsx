import { useState, useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { fetchAPIData } from "./redux/slices/dataSlice";

import Home from "./pages/home/Home";
import Header from "./components/Header";
import "./App.css";

function App() {
  const [menuOpen, setMenuOpen] = useState(false);
  const dispatch = useDispatch();
  const data = useSelector(state => state.data.data);
  const isLoading = useSelector(state => state.data.isLoading);
  const error = useSelector(state => state.data.error);

  useEffect(() => {
    dispatch(fetchAPIData());
  }, [dispatch]);

  const handleChangeHeaderToggleSwitch = () => {
    setMenuOpen((prevState) => !prevState);
  };

  return (
    <>
      <Header
        menuOpen={menuOpen}
        onChangeHeaderToggleSwitch={handleChangeHeaderToggleSwitch}
        nameOfPage={"Главная страница"}
      />
      <div className={`content-container ${menuOpen ? "menu-open" : ""}`}>
        {isLoading ? (
          <div>Loading...</div>
        ) : error ? (
          <div>Error: {error}</div>
        ) : (
          <Home data={data} />
        )}
      </div>
    </>
  );
}

export default App;
