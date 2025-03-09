import * as yup from "yup";

const PHONE_REGEX = /^\d{6,15}$/;

const ALLOWED_FILE_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
];
const MAX_FILE_SIZE = 5 * 1024 * 1024;

export const schema = yup.object({
    first_name: yup.string().required("First Name is required"),
    last_name: yup.string().required("Last Name is required"),
    email: yup
        .string()
        .email("Please enter a valid email")
        .required("Email is required"),
    phone: yup
        .string()
        .required("Phone number is required")
        .matches(PHONE_REGEX, "Please enter a valid phone number"),

    cv: yup
        .mixed()
        .test(
            "fileSize",
            `File size must be less than ${MAX_FILE_SIZE / (1024 * 1024)}MB`,
            (value) =>
                value && value.length > 0
                    ? value[0].size <= MAX_FILE_SIZE
                    : false
        )
        .test(
            "fileType",
            `Only pdf or docx allowed`,
            (value) =>
                value && value.length > 0
                    ? ALLOWED_FILE_TYPES.includes(value[0].type)
                    : false
        )
        .required("Please upload you CV"),
});
