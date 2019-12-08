import React, { Component, Fragment } from 'react';
import ReactDOM from 'react-dom';
import api from './api';
import OptionField from './Components/OptionField';
import ProgessBar from './Components/ProgessBar';

class App extends Component {
  state = {
    isLoading: true,
    formData: {
      categories: [],
      modelData: {
        models: [
          {
            id: null,
          },
        ],
      },
      categoriesData: {
        bodystyles: [],
        brands: [],
        geartypes: [],
        models: [],
      },
    },
    category_id: null,
    bodystyle: null,
    marka_id: null,
    gearbox: null,
    model_id: null,
  };

  componentDidMount() {
    api.get('category/').then(res => {
      this.setState({
        formData: { ...this.state.formData, categories: res.data },
        isLoading: !this.state.isLoading,
        category_id: res.data[0].id,
      });
      api.get(`category/${res.data[0].id}`).then(
        res => (
          this.setState({
            formData: {
              ...this.state.formData,
              categoriesData: res.data,
            },
            bodystyle: res.data.bodystyles[0].id,
            marka_id: res.data.brands[0].id,
            gearbox: res.data.geartypes[0].id,
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
        formData: {
          ...this.state.formData,
          modelData: res.data,
        },
        model_id: res.data.models[0].id,
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

  onSubmit = e => {
    e.preventDefault();
    const { category_id, bodystyle, marka_id, gearbox, model_id } = this.state;
    const data = { category_id, bodystyle, marka_id, gearbox, model_id };
    api.post('/create_monitoring', data);
  };

  render() {
    const { isLoading } = this.state;
    const { categories, categoriesData, modelData } = this.state.formData;
    return (
      <div className="container">
        {isLoading ? (
          <ProgessBar />
        ) : (
          <form
            onSubmit={this.onSubmit}
            className="text-center border border-light p-5"
          >
            <p className="h4 mb-4">Создать новый мониоринг</p>
            <OptionField
              title="Тип автомобиля"
              name="category_id"
              onChange={this.onChangeCategory}
              options={categories}
            />
            <OptionField
              title="Марка"
              name="marka_id"
              onChange={this.onChangeBrand}
              options={categoriesData.brands}
            />
            <OptionField
              title="Модель"
              name="model_id"
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
              name="gearbox"
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
