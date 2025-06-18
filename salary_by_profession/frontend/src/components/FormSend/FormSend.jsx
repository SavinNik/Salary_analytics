import React, { useState, useEffect } from 'react';

export const FormSend = () => {
  const [salaryFrom, setSalaryFrom] = useState('');
  const [salaryTo, setSalaryTo] = useState('');
  const [professions, setProfessions] = useState([]);
  const [selectedPosition, setSelectedPosition] = useState('');

  // Загрузка списка профессий
  useEffect(() => {
    fetch("http://localhost:8000/api/v1/professions")
      .then((response) => response.json())
      .then(data => {
        setProfessions(data.professions);
      })
      .catch(err => console.error("Ошибка загрузки профессий:", err));
  }, []);

  // При выборе другой профессии очищаем зарплату
  const handleSelectChange = (e) => {
    setSelectedPosition(e.target.value);
    setSalaryFrom('');
    setSalaryTo('');
  };

  // Получение зарплаты по выбранной профессии
  const handleGetSalary = async (e) => {
    e.preventDefault();
    if (!selectedPosition) return;

    try {
      const response = await fetch(`http://localhost:8000/api/v1/salary/${selectedPosition}`);
      if (!response.ok) throw new Error("Профессия не найдена");

      const data = await response.json();
      setSalaryFrom(data.salary_from);
      setSalaryTo(data.salary_to);
    } catch (err) {
      alert(`Ошибка: ${err.message}`);
      console.error(err);
    }
  };

  // Очистка формы
  const handleClear = (e) => {
    e.preventDefault();
    setSelectedPosition('');
    setSalaryFrom('');
    setSalaryTo('');
  };

  return (
    <div className='formsend'>
      <form>
        <label htmlFor="vacancy-select">Ваша профессия: </label>
        <select
          id="vacancy-select"
          value={selectedPosition}
          onChange={handleSelectChange}
        >
          <option value="">-- Выберите профессию --</option>
          {professions.map((profession) => (
            <option key={profession} value={profession}>
              {profession}
            </option>
          ))}
        </select>

        <button className='btn get-salary' onClick={handleGetSalary}>Узнать зарплату</button>
      </form>

      {salaryFrom && (
        <div>
          <div className='salary'>
            {(Math.round(salaryFrom / 1000) * 1000).toLocaleString()} - {(Math.round(salaryTo / 1000) * 1000).toLocaleString()} руб.
          </div>
          <button className='btn clear' onClick={handleClear}>Сбросить</button>
        </div>
      )}
    </div>
  );
};