export default [
    {
      files: ["**/*.js"],
      languageOptions: {
        ecmaVersion: 2021,
        globals: { node: "readonly", jest: "readonly" }
      },
      rules: {
        "no-unused-vars": "warn"
      }
    }
  ];
  