from src.analytics.demand_analysis import save_hourly_demand
from src.analytics.zone_consumption import save_zone_consumption
from src.analytics.ufg_analysis import save_ufg_results
from src.analytics.pressure_analysis import save_pressure_violations
from src.analytics.sensor_health_analysis import save_sensor_health
from src.analytics.leak_statistics import save_leak_statistics


def run_analytics():
    save_hourly_demand()
    save_zone_consumption()
    save_ufg_results()
    save_pressure_violations()
    save_sensor_health()
    save_leak_statistics()
    print('Analytics outputs generated to data/analytics_outputs')

if __name__ == '__main__':
    run_analytics()
