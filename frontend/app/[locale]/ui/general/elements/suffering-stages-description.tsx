import { getI18n } from "@/locales/server";

type SufferingScaleDescriptionProps = {
    display_criteria?: boolean;
}

interface SufferingStage {
    title: string;
    stage_description: string;
    criteria_description: string;
    background_color: string;
    border_color?: string;
    text_color?:'light' | 'dark';
}

export default async function SufferingStagesDescription({display_criteria = false}: SufferingScaleDescriptionProps) {
    const t = await getI18n();

    const suffering_stages: SufferingStage[] = [
        {
            title: t('PainEquationSection.stages.discomfort.title'),
            stage_description: t('PainEquationSection.stages.discomfort.text'),
            criteria_description: t('MethodologyPage.sufferingQuantificationSteps.legend.discomfort.criteria_description'),
            background_color: 'pink-1',
            border_color: 'pink-2',
        },
        {
            title: t('PainEquationSection.stages.pain.title'),
            stage_description: t('PainEquationSection.stages.pain.text'),
            criteria_description: t('MethodologyPage.sufferingQuantificationSteps.legend.pain.criteria_description'),
            background_color: 'pink-2',
        },
        {
            title: t('PainEquationSection.stages.suffering.title'),
            stage_description: t('PainEquationSection.stages.suffering.text'),
            criteria_description: t('MethodologyPage.sufferingQuantificationSteps.legend.suffering.criteria_description'),
            background_color: 'pink-3',
        },
        {
            title: t('PainEquationSection.stages.agony.title'),
            stage_description: t('PainEquationSection.stages.agony.text'),
            criteria_description: t('MethodologyPage.sufferingQuantificationSteps.legend.agony.criteria_description'),
            background_color: 'brown',
            text_color: 'light',
        },

    ]


    return (
        <div className="grid grid-cols-1 md:grid-cols-4 ">
            {
                suffering_stages.map((suffering_stage: SufferingStage) => {
                    const border_color_class = suffering_stage.border_color ? `border border-${suffering_stage.border_color}` : '';

                    const text_color_class = suffering_stage.text_color ? `${suffering_stage.text_color}-text` : 'dark-text';

                    const background_color_class = `bg-${suffering_stage.background_color}`;

                    return (
                    <article className={`p-4 ${background_color_class} ${border_color_class} ${text_color_class}`}>
                        <h4 className="font-bold uppercase mb-4 mt-4">{suffering_stage.title}</h4>
                        <p className="text-sm font-medium">{suffering_stage.stage_description}</p>
                        {display_criteria && <p className="pt-2">
                    <span
                        className="text-sm font-bold">{t('MethodologyPage.sufferingQuantificationSteps.criteria')} : </span>
                            <span
                                className={`text-sm`}>{suffering_stage.criteria_description}</span>
                        </p>}
                    </article>
                )})
            }
        </div>
    )
}
