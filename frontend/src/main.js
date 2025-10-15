// tsconfig.app.json (Application-Specific Configuration)
{
  "extends": "./tsconfig.json", // Correctly extends the base file
  "compilerOptions": {
    "lib": ["DOM", "DOM.Iterable", "ES2020"], // Browser-specific libs
    "jsx": "react-jsx",
    "noEmit": true,
    "isolatedModules": true
  },
  "include": ["src"]
}