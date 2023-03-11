import { create } from "zustand";

const useCitiesStore = create((set) => ({
	cities: [],
	setCities: (cities) =>
		set((state) => ({
			cities: [...cities],
		})),
}));

export default useCitiesStore;
