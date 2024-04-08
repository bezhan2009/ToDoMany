//import { useGetAllDataQuery } from "./redux/services/dataSlice";
import { useDispatch, useSelector } from "react-redux";
import { toggleMenu, selectIsMenuOpen } from "./redux/slices/menuOpenSlice";

import Home from "./pages/home/Home";
import Header from "./components/Header";
import "./App.css";

function App() {
  const menuOpen = useSelector(selectIsMenuOpen);
  const dispatch = useDispatch();

  //const { isLoading, error, data } = useGetAllDataQuery("/");

  const handleChangeHeaderToggleSwitch = () => {
    dispatch(toggleMenu());
  };

  return (
    <>
      <Header
        menuOpen={menuOpen}
        onChangeHeaderToggleSwitch={handleChangeHeaderToggleSwitch}
        nameOfPage={"Главная страница"}
      />
      <div className={`content-container ${menuOpen ? "menu-open" : ""}`}>
        {/* {error ? (
        <>Oh no, there was an error</>
      ) : isLoading ? (
        <>Loading...</>
      ) : data ? (
        <>
          <Home />
        </>
      ) : null} */}
        <Home />
      </div>
    </>
  );
}

export default App;
