class EMSPipeline:
    async def run(self, inputs):

        features = self.build_features(inputs)

        forecast = self.forecast_engine.run(features)

        simulation = self.simulation_engine.run(forecast)

        decision = self.decision_engine.run(
            forecast,
            simulation,
            self.state
        )

        self.memory.update(inputs, forecast, decision)

        return {
            "forecast": forecast,
            "simulation": simulation,
            "decision": decision,
        }
