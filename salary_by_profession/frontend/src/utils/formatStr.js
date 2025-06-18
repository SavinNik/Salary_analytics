export function formatString(str) {
  const formattedString = [];
  const len = str.length;
  for (let i = len - 1; i >= 0; i--) {
    formattedString.push(str[i]);
    if ((len - i) % 3 === 0 && i !== 0) {
      formattedString.push(' ');
    }
  }
  return formattedString.reverse().join('');
}

// Пример использования
// const inputString = "123456789012345";
// const formattedString = formatString(inputString);
// console.log(formattedString); // Вывод: 123 456 789 012 345