from src.ml.leak_prediction import train_leak_model
from src.ml.demand_forecast import generate_30d_demand_forecast


def run_ml():
    leak_metrics = train_leak_model()
    print('Leak prediction model trained:')
    print('accuracy:', leak_metrics['accuracy'])

    forecast = generate_30d_demand_forecast()
    print('Demand forecast generated:', len(forecast), 'rows')

    print('ML pipeline complete.')

if __name__ == "__main__":
    run_ml()
