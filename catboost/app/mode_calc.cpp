#include <catboost/libs/app_helpers/mode_calc_helpers.h>
#include <catboost/libs/model/model.h>

namespace {
    class TOpenSourceModeCalcImplementation : public NCB::IModeCalcImplementation {
        int mode_calc(int argc, const char** argv) const override {
            NCB::TAnalyticalModeCommonParams params;
            size_t iterationsLimit = 0;
            size_t evalPeriod = 0;
            auto parser = NLastGetopt::TOpts();

            NCB::PrepareCalcModeParamsParser(&params, &iterationsLimit, &evalPeriod, &parser);
            NLastGetopt::TOptsParseResult parserResult{&parser, argc, argv};

            TFullModel model;
            ReadModelAndUpdateParams(&params, &iterationsLimit, &evalPeriod, &model);

            NCB::CalcModelSingleHost(params, iterationsLimit, evalPeriod, model);

            return 0;
        }
    };
}

NCB::TModeCalcImplementationFactory::TRegistrator<TOpenSourceModeCalcImplementation> YandexSpecificModeCalcImplementationRegistrator(NCB::EImplementationType::OpenSource);
