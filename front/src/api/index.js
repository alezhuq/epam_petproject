import axios from "axios";
import { QueryClient } from "react-query";

export const $host = axios.create({
	baseURL: process.env.API_URL,
});

export const queryClient = new QueryClient({
	defaultOptions: {
		queries: {
			refetchOnWindowFocus: false,
		},
	},
});
