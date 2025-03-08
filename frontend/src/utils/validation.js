import * as yup from "yup";

export const schema = yup.object({
    name: yup.string().required("Name is required"),
    email: yup.string().email("Invalid email").required("Email is required"),
    phone: yup
        .string()
        .matches(/^[0-9]{10}$/, "Phone number must be 10 digits")
        .required("Phone number is required"),
    cv: yup
        .mixed()
        .test("fileSize", "File size must be less than 10MB", (value) =>
            value && value.length > 0
                ? value[0].size <= 10 * 1024 * 1024
                : false
        )
        .test("fileType", "Only PDF or DOCX allowed", (value) =>
            value && value.length > 0
                ? [
                      "application/pdf",
                      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                  ].includes(value[0].type)
                : false
        )
        .required("CV is required"),
});
