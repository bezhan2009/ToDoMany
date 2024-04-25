import React, { useEffect } from "react";
import '../css/registration.css';
const Regis = () => {
    return (
        <div class='html'>
        <form class="form_regis">
            <h1>Добро пожаловать</h1>
            <div class="cont">
                <div class="input_cont">
                    <input type="email" placeholder="Логин" class="text-input" id="loginInput"/>
                    <input type="password" placeholder="Пароль" class="text-input" id="passwordInput1"/>
                    <input type="password" placeholder="Подтвердите пароль" class="text-input" id="passwordInput2"/>
                </div>
                <button class="btnRegister">Регистрация</button>
                <div class="if_cont">
                    <p>Есть аккаунт?</p> <a class="login" href="/login">Вход</a>
                </div>
            </div>
        </form>
        </div>
    );
};

export default Regis;