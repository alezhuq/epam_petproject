import React from "react";
import InstagramIcon from "@mui/icons-material/Instagram";
import FacebookOutlinedIcon from "@mui/icons-material/FacebookOutlined";
import YouTubeIcon from "@mui/icons-material/YouTube";
import LocalPhoneIcon from "@mui/icons-material/LocalPhone";
import { NavLink } from "react-router-dom";

const isActiveNav = ({ isActive }) => {
	return isActive ? "active" : "default";
};

function Footer() {
	return (
		<div className="footer">
			<div className="footer__menu _container">
				<ul className="footer__list">
					<li className="footer__list__item">
						<NavLink to="/create/company" className={isActiveNav}>
							додати компанію
						</NavLink>
					</li>
					<li className="footer__list__item">
						<NavLink to="/create/city" className={isActiveNav}>
							додати місто
						</NavLink>
					</li>
					<li className="footer__list__item">
						<NavLink to="/create/service" className={isActiveNav}>
							додати послугу
						</NavLink>
					</li>
					<li className="footer__list__item">
						<NavLink to="/contacts" className={isActiveNav}>
							контакти
						</NavLink>
					</li>
					<li className="footer__list__item">
						<div className="phone">
							<LocalPhoneIcon />
							&nbsp;
							<span className="number">
								<a className="number__link" href="tel:+380675551673">
									+38 067 555 1673
								</a>
							</span>
						</div>
					</li>
					<li className="footer__list__item">
						<a href="#">
							<FacebookOutlinedIcon sx={{ color: "#F5FBFE" }} />
						</a>
					</li>
					<li className="footer__list__item">
						<a href="#">
							<InstagramIcon sx={{ color: "#F5FBFE" }} />
						</a>
					</li>
					<li className="footer__list__item">
						<a href="#">
							<YouTubeIcon sx={{ color: "#F5FBFE" }} />
						</a>
					</li>
				</ul>
				<div className="footer__description">
					ПП “YEZZ Group” 2023 Всі права захищено
				</div>
			</div>
		</div>
	);
}

export default Footer;
