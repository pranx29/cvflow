import axios from "axios";

export const submitApplication = async (formData) => {
    try {
        const response = await axios.post(
            "http://127.0.0.1:8000/api/job-application/submit",
            formData,
            {
                headers: { "Content-Type": "multipart/form-data" },
            }
        );
        return response;
    } catch (error) {
        throw error;
    }
};
