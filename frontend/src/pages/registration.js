import React, { useEffect } from "react";
import '../css/registration.css';
const Regis = () => {
    return (
        <div className='html'>
            <form className="form_regis">
                <h1>Добро пожаловать</h1>
                <div className="cont">
                    <div className="input_cont">
                        <input type="email" placeholder="Логин" className="text-input" id="loginInput" />
                        <input type="password" placeholder="Пароль" className="text-input" id="passwordInput1" />
                        <input type="password" placeholder="Подтвердите пароль" className="text-input" id="passwordInput2" />
                    </div>
                    <button className="btnRegister">Регистрация</button>
                    <div className="if_cont">
                        <p>Есть аккаунт?</p> <a className="login" href="/login">Вход</a>
                    </div>
                </div>
            </form>
        </div>
    );
};

export default Regis;