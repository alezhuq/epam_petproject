import React from "react";
import { Link, NavLink } from "react-router-dom";
import InstagramIcon from "@mui/icons-material/Instagram";
import FacebookOutlinedIcon from "@mui/icons-material/FacebookOutlined";
import YouTubeIcon from "@mui/icons-material/YouTube";
import LocalPhoneIcon from "@mui/icons-material/LocalPhone";

function toggleBurger() {
	document.querySelector(".header__burger").classList.toggle("active");
	document.querySelector(".header__menu").classList.toggle("active");
	document.body.classList.toggle("lock");
}
function closeBurger() {
	if (document.querySelector(".header__burger").classList.contains("active")) {
		document.body.classList.remove("lock");
		document.querySelector(".header__burger").classList.remove("active");
		document.querySelector(".header__menu").classList.remove("active");
	}
}

const isActiveNav = ({ isActive }) => {
	return isActive ? "active" : "default";
};

function Header() {
	return (
		<div className="header">
			<div className="header__container _container">
				<Link to="/" className="header__logo__link" onClick={closeBurger}>
					<h1 className="header__logo">YEZZ CATALOG</h1>
				</Link>
				<div className="header__burger" onClick={toggleBurger}>
					<span></span>
				</div>
				<div className="header__menu">
					<ul className="menu__list">
						<li className="menu__item">
							<NavLink to="/" className={isActiveNav} onClick={closeBurger}>
								Каталог
							</NavLink>
						</li>
						<li className="menu__item">
							<NavLink
								to="/contacts"
								className={isActiveNav}
								onClick={closeBurger}
							>
								контакти
							</NavLink>
						</li>

						<li className="menu__item">
							<a href="#">
								<FacebookOutlinedIcon sx={{ color: "#F5FBFE" }} />
							</a>
						</li>

						<li className="menu__item">
							<a href="#">
								<InstagramIcon sx={{ color: "#F5FBFE" }} />
							</a>
						</li>

						<li className="menu__item">
							<a href="#">
								<YouTubeIcon sx={{ color: "#F5FBFE" }} />
							</a>
						</li>
					</ul>
				</div>
			</div>
		</div>
	);
}

export default Header;
