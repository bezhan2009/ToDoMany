import { useDispatch, useSelector } from "react-redux";
import { Routes, Route } from "react-router-dom";
import { toggleMenu, selectIsMenuOpen } from "@redux/slices/menuOpenSlice";

import { Home, ErrorPage, EnvironmentPage } from "@pages/index.jsx";
import Header from "@components/header/Header.jsx";
import "./App.scss";

function App() {
  const menuOpen = useSelector(selectIsMenuOpen);
  const dispatch = useDispatch();

  // const { isLoading, error, data } = useGetAllDataQuery("api/environment/");
  // console.log(error);

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
          <>Oh no, there was an error^ </>
        ) : isLoading ? (
          <>Loading...</>
        ) : data ? (
          <>
            <Home />
          </>
        ) : null} */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/demo/api/environment/:id" element={<EnvironmentPage />} />
          <Route path="*" element={<ErrorPage error="404" />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
