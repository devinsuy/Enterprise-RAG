module.exports = {
    env: {
      browser: true,
      es2021: true
    },
    extends: [
      'prettier',
      'react-app',
      'plugin:react/recommended',
      'plugin:react-hooks/recommended',
      'standard-with-typescript'
    ],
    overrides: [],
    parserOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      tsconfigRootDir: __dirname,
      project: ['tsconfig.json']
    },
    plugins: ['react'],
    rules: {
      'react/react-in-jsx-scope': 'off',
      '@typescript-eslint/space-before-function-paren': 'off',
      '@typescript-eslint/explicit-function-return-type': 'off',
      '@typescript-eslint/no-unused-vars': 'warn',
      '@typescript-eslint/no-floating-promises': 'off',
      '@typescript-eslint/strict-boolean-expressions': 'off',
      '@typescript-eslint/no-empty-interface': 'off',
      '@typescript-eslint/promise-function-async': 'off',
      '@typescript-eslint/no-misused-promises': 'off',
      '@typescript-eslint/comma-dangle': 'off'
    }
  }
  