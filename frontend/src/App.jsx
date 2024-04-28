import { useGetAllDataQuery } from "./redux/services/dataSlice";
import { useDispatch, useSelector } from "react-redux";
import { Routes, Route } from "react-router-dom";
import { toggleMenu, selectIsMenuOpen } from "@redux/slices/menuOpenSlice";

import { Home, ErrorPage, EnviromentPage } from "@pages/index.jsx";
import Header from "@components/header/Header.jsx";
import "./App.scss";

function App() {
  const menuOpen = useSelector(selectIsMenuOpen);
  const dispatch = useDispatch();

  const { isLoading, error, data } = useGetAllDataQuery();
  console.log(data);
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
      {error ? (
          <>Oh no, there was an error^ </>
        ) : isLoading ? (
          <>Loading...</>
        ) : data ? (
          <>
            <Home />
          </>
        ) : null}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/demo/api/enviroment/:id" element={<EnviromentPage />} />
        <Route path="*" element={<ErrorPage error="404" />} />
      </Routes>
    </>
  );
}

export default App;
