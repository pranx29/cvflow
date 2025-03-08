import axios from "axios";

export const submitApplication = async (formData) => {
    try {
        const response = await axios.post(
            "http://127.0.0.1:8000/api/submit-application",
            formData,
            {
                headers: { "Content-Type": "multipart/form-data" },
            }
        );
        return response.data;
    } catch (error) {
        console.error("API error:", error);
        throw error;
    }
};
