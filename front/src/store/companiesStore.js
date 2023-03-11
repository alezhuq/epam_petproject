import {create} from "zustand";

const useCompaniesStore = create((set)=>({
    companies: [],
    setCompanies: (companies)=> set( state => (
        {
            companies: [
                ...companies
            ]
        }
    )),

}))

export default useCompaniesStore;