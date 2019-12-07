import React from 'react';

function OptionField({ title, name, onChange, options }) {
  return (
    <React.Fragment>
      <label>{title}</label>
      <select
        name={name}
        onChange={onChange}
        className="browser-default custom-select mb-4"
      >
        <option value="" disabled>
          Выберите опцию
        </option>
        {options.map((el, index) => (
          <option key={el.id} value={el.id}>
            {el.name}
          </option>
        ))}
      </select>
    </React.Fragment>
  );
}

export default OptionField;
