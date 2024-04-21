import { useGetAllDataQuery } from "./redux/services/dataSlice";
import { useDispatch, useSelector } from "react-redux";
import { toggleMenu, selectIsMenuOpen } from "./redux/slices/menuOpenSlice";
import { Routes, Route } from "react-router-dom";

import Home from "./pages/home/Home";
import ErrorPage from "./pages/errorPage/ErrorPage.jsx";
import EnviromentPage from "./pages/enviroment/EnviromentTask.jsx";
import Header from "./components/header/Header.jsx";
import "./App.scss";

function App() {
  const menuOpen = useSelector(selectIsMenuOpen);
  const dispatch = useDispatch();

  const { isLoading, error, data } = useGetAllDataQuery("api/environment/");
  console.log(error);

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
        {error ? (
          <>Oh no, there was an error^ </>
        ) : isLoading ? (
          <>Loading...</>
        ) : data ? (
          <>
            <Home />
          </>
        ) : null}
        {/* <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/demo/api/enviroment/:id" element={<EnviromentPage />} />
          <Route path="*" element={<ErrorPage error="404" />} />
        </Routes> */}
      </div>
    </>
  );
}

export default App;
