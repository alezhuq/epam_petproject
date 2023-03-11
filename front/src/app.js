import React, { useEffect } from "react";
import "./styles/style.scss";
import { BrowserRouter, Routes, Route, useLocation } from "react-router-dom";
import Line from "./components/Line";
import Header from "./components/Header";
import Footer from "./components/Footer";
const Contacts = React.lazy(() => import("./pages/Contacts"));
const Catalog = React.lazy(() => import("./pages/Catalog"));
const ErrorPage = React.lazy(() => import("./pages/ErrorPage"));
const Product = React.lazy(() => import("./components/catalogpages/Product"));
const CreateCity = React.lazy(() => import("./pages/CreateCity"));
const CreateService = React.lazy(() => import("./pages/CreateService"));
const CreateCompany = React.lazy(() => import("./pages/CreateCompany"));

function ScrollToTop() {
	const { pathname } = useLocation();

	useEffect(() => {
		window.scrollTo(0, 0);
	}, [pathname]);

	return null;
}

function app() {
	return (
		<BrowserRouter>
			<ScrollToTop />
			<Header />
			<Line />
			<Routes>
				<Route
					path="/"
					element={
						<React.Suspense>
							<Catalog />
						</React.Suspense>
					}
				/>
				<Route
					path="/search/:keyword"
					element={
						<React.Suspense>
							<Catalog />
						</React.Suspense>
					}
				/>
				<Route
					path="/filter/:cities"
					element={
						<React.Suspense>
							<Catalog />
						</React.Suspense>
					}
				/>
				<Route
					path="/contacts"
					element={
						<React.Suspense>
							<Contacts />
						</React.Suspense>
					}
				/>
				<Route
					path="*"
					element={
						<React.Suspense>
							<ErrorPage
								title={"Схоже такої сторінки не існує"}
								text={"Головне меню"}
								link={"/"}
							/>
						</React.Suspense>
					}
				/>
				<Route
					path="/product/:id"
					element={
						<React.Suspense>
							<Product />
						</React.Suspense>
					}
				/>
				<Route
					path="/create/city"
					element={
						<React.Suspense>
							<CreateCity />
						</React.Suspense>
					}
				/>
				<Route
					path="/create/company"
					element={
						<React.Suspense>
							<CreateCompany />
						</React.Suspense>
					}
				/>
				<Route
					path="/create/service"
					element={
						<React.Suspense>
							<CreateService />
						</React.Suspense>
					}
				/>
			</Routes>
			<Footer />
		</BrowserRouter>
	);
}

export default app;
