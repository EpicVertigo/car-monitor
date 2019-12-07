import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import api from './api';
import OptionField from './Components/OptionField';

class App extends Component {
  state = {
    isLoading: true,
    formData: {
      categories: [],
      modelData: {
        models: [],
      },
      categoriesData: {
        bodystyles: [],
        brands: [],
        geartypes: [],
        models: [],
      },
    },
    category: null,
    bodystyle: null,
    brand: null,
    geartype: null,
    model: null,
  };

  componentDidMount() {
    api.get('category/').then(res => {
      this.setState({
        formData: { ...this.state.formData, categories: res.data },
        isLoading: !this.state.isLoading,
      });
      api.get(`category/${res.data[0].id}`).then(
        res => (
          this.setState({
            formData: { ...this.state.formData, categoriesData: res.data },
          }),
          this.getModels(res.data.brands[0].id)
        ),
      );
    });
  }

  onChange = e => this.setState({ [e.target.name]: e.target.value });

  getModels = brandId => {
    api.get(`brands/${brandId}`).then(res =>
      this.setState({
        formData: { ...this.state.formData, modelData: res.data },
      }),
    );
  };

  onChangeCategory = e => {
    const id = e.target.value;
    this.setState({ [e.target.name]: id });
    api.get(`category/${id}`).then(res =>
      this.setState({
        formData: { ...this.state.formData, modelData: res.data },
      }),
    );
  };

  onChangeBrand = e => {
    const id = e.target.value;
    this.setState({ [e.target.name]: id });
    this.getModels(id);
  };

  render() {
    const { isLoading } = this.state;
    const { categories, categoriesData, modelData } = this.state.formData;
    return (
      <div className="container">
        {isLoading ? (
          <div className="progress">
            <div
              className="progress-bar progress-bar-indeterminate"
              role="progressbar"
            ></div>
          </div>
        ) : (
          <form className="text-center border border-light p-5" action="#!">
            <p className="h4 mb-4">Создать новый мониоринг</p>

            <label>Тип автомобиля</label>
            <select
              name="category"
              onChange={this.onChangeCategory}
              className="browser-default custom-select mb-4"
            >
              <option value="" disabled>
                Выберите опцию
              </option>
              {categories.map((el, index) => (
                <option
                  disabled={el.id !== 1 ? 'on' : null}
                  key={el.id}
                  value={el.id}
                >
                  {el.name}
                </option>
              ))}
            </select>

            <OptionField
              title="Марка"
              name="brand"
              onChange={this.onChangeBrand}
              options={categoriesData.brands}
            />

            <OptionField
              title="Модель"
              name="model"
              onChange={this.onChange}
              options={modelData.models}
            />

            <OptionField
              title="Тип кузова"
              name="bodystyle"
              onChange={this.onChange}
              options={categoriesData.bodystyles}
            />

            <OptionField
              title="Коробка передач"
              name="geartype"
              onChange={this.onChange}
              options={categoriesData.geartypes}
            />

            <button className="btn btn-info btn-block">Создать</button>
          </form>
        )}
      </div>
    );
  }
}

ReactDOM.render(<App />, document.getElementById('app'));
