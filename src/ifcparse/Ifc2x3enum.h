/********************************************************************************
 *                                                                              *
 * This file is part of IfcOpenShell.                                           *
 *                                                                              *
 * IfcOpenShell is free software: you can redistribute it and/or modify         *
 * it under the terms of the Lesser GNU General Public License as published by  *
 * the Free Software Foundation, either version 3.0 of the License, or          *
 * (at your option) any later version.                                          *
 *                                                                              *
 * IfcOpenShell is distributed in the hope that it will be useful,              *
 * but WITHOUT ANY WARRANTY; without even the implied warranty of               *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                 *
 * Lesser GNU General Public License for more details.                          *
 *                                                                              *
 * You should have received a copy of the Lesser GNU General Public License     *
 * along with this program. If not, see <http://www.gnu.org/licenses/>.         *
 *                                                                              *
 ********************************************************************************/

/********************************************************************************
 *                                                                              *
 * This file has been generated from IFC2X3_TC1.exp. Do not make modifications  *
 * but instead modify the python script that has been used to generate this.    *
 *                                                                              *
 ********************************************************************************/

#ifndef IFC2X3ENUM_H
#define IFC2X3ENUM_H

#include "../ifcparse/IfcParse_Export.h"

#define IfcSchema Ifc2x3

namespace Ifc2x3 {

namespace Type {
    typedef enum {
        Ifc2DCompositeCurve, IfcAbsorbedDoseMeasure, IfcAccelerationMeasure, IfcActionRequest, IfcActionSourceTypeEnum, IfcActionTypeEnum, IfcActor, IfcActorRole, IfcActorSelect, IfcActuatorType, IfcActuatorTypeEnum, IfcAddress, IfcAddressTypeEnum, IfcAheadOrBehind, IfcAirTerminalBoxType, IfcAirTerminalBoxTypeEnum, IfcAirTerminalType, IfcAirTerminalTypeEnum, IfcAirToAirHeatRecoveryType, IfcAirToAirHeatRecoveryTypeEnum, IfcAlarmType, IfcAlarmTypeEnum, IfcAmountOfSubstanceMeasure, IfcAnalysisModelTypeEnum, IfcAnalysisTheoryTypeEnum, IfcAngularDimension, IfcAngularVelocityMeasure, IfcAnnotation, IfcAnnotationCurveOccurrence, IfcAnnotationFillArea, IfcAnnotationFillAreaOccurrence, IfcAnnotationOccurrence, IfcAnnotationSurface, IfcAnnotationSurfaceOccurrence, IfcAnnotationSymbolOccurrence, IfcAnnotationTextOccurrence, IfcApplication, IfcAppliedValue, IfcAppliedValueRelationship, IfcAppliedValueSelect, IfcApproval, IfcApprovalActorRelationship, IfcApprovalPropertyRelationship, IfcApprovalRelationship, IfcArbitraryClosedProfileDef, IfcArbitraryOpenProfileDef, IfcArbitraryProfileDefWithVoids, IfcAreaMeasure, IfcArithmeticOperatorEnum, IfcAssemblyPlaceEnum, IfcAsset, IfcAsymmetricIShapeProfileDef, IfcAxis1Placement, IfcAxis2Placement, IfcAxis2Placement2D, IfcAxis2Placement3D, IfcBSplineCurve, IfcBSplineCurveForm, IfcBeam, IfcBeamType, IfcBeamTypeEnum, IfcBenchmarkEnum, IfcBezierCurve, IfcBlobTexture, IfcBlock, IfcBoilerType, IfcBoilerTypeEnum, IfcBoolean, IfcBooleanClippingResult, IfcBooleanOperand, IfcBooleanOperator, IfcBooleanResult, IfcBoundaryCondition, IfcBoundaryEdgeCondition, IfcBoundaryFaceCondition, IfcBoundaryNodeCondition, IfcBoundaryNodeConditionWarping, IfcBoundedCurve, IfcBoundedSurface, IfcBoundingBox, IfcBoxAlignment, IfcBoxedHalfSpace, IfcBuilding, IfcBuildingElement, IfcBuildingElementComponent, IfcBuildingElementPart, IfcBuildingElementProxy, IfcBuildingElementProxyType, IfcBuildingElementProxyTypeEnum, IfcBuildingElementType, IfcBuildingStorey, IfcCShapeProfileDef, IfcCableCarrierFittingType, IfcCableCarrierFittingTypeEnum, IfcCableCarrierSegmentType, IfcCableCarrierSegmentTypeEnum, IfcCableSegmentType, IfcCableSegmentTypeEnum, IfcCalendarDate, IfcCartesianPoint, IfcCartesianTransformationOperator, IfcCartesianTransformationOperator2D, IfcCartesianTransformationOperator2DnonUniform, IfcCartesianTransformationOperator3D, IfcCartesianTransformationOperator3DnonUniform, IfcCenterLineProfileDef, IfcChamferEdgeFeature, IfcChangeActionEnum, IfcCharacterStyleSelect, IfcChillerType, IfcChillerTypeEnum, IfcCircle, IfcCircleHollowProfileDef, IfcCircleProfileDef, IfcClassification, IfcClassificationItem, IfcClassificationItemRelationship, IfcClassificationNotation, IfcClassificationNotationFacet, IfcClassificationNotationSelect, IfcClassificationReference, IfcClosedShell, IfcCoilType, IfcCoilTypeEnum, IfcColour, IfcColourOrFactor, IfcColourRgb, IfcColourSpecification, IfcColumn, IfcColumnType, IfcColumnTypeEnum, IfcComplexNumber, IfcComplexProperty, IfcCompositeCurve, IfcCompositeCurveSegment, IfcCompositeProfileDef, IfcCompoundPlaneAngleMeasure, IfcCompressorType, IfcCompressorTypeEnum, IfcCondenserType, IfcCondenserTypeEnum, IfcCondition, IfcConditionCriterion, IfcConditionCriterionSelect, IfcConic, IfcConnectedFaceSet, IfcConnectionCurveGeometry, IfcConnectionGeometry, IfcConnectionPointEccentricity, IfcConnectionPointGeometry, IfcConnectionPortGeometry, IfcConnectionSurfaceGeometry, IfcConnectionTypeEnum, IfcConstraint, IfcConstraintAggregationRelationship, IfcConstraintClassificationRelationship, IfcConstraintEnum, IfcConstraintRelationship, IfcConstructionEquipmentResource, IfcConstructionMaterialResource, IfcConstructionProductResource, IfcConstructionResource, IfcContextDependentMeasure, IfcContextDependentUnit, IfcControl, IfcControllerType, IfcControllerTypeEnum, IfcConversionBasedUnit, IfcCooledBeamType, IfcCooledBeamTypeEnum, IfcCoolingTowerType, IfcCoolingTowerTypeEnum, IfcCoordinatedUniversalTimeOffset, IfcCostItem, IfcCostSchedule, IfcCostScheduleTypeEnum, IfcCostValue, IfcCountMeasure, IfcCovering, IfcCoveringType, IfcCoveringTypeEnum, IfcCraneRailAShapeProfileDef, IfcCraneRailFShapeProfileDef, IfcCrewResource, IfcCsgPrimitive3D, IfcCsgSelect, IfcCsgSolid, IfcCurrencyEnum, IfcCurrencyRelationship, IfcCurtainWall, IfcCurtainWallType, IfcCurtainWallTypeEnum, IfcCurvatureMeasure, IfcCurve, IfcCurveBoundedPlane, IfcCurveFontOrScaledCurveFontSelect, IfcCurveOrEdgeCurve, IfcCurveStyle, IfcCurveStyleFont, IfcCurveStyleFontAndScaling, IfcCurveStyleFontPattern, IfcCurveStyleFontSelect, IfcDamperType, IfcDamperTypeEnum, IfcDataOriginEnum, IfcDateAndTime, IfcDateTimeSelect, IfcDayInMonthNumber, IfcDaylightSavingHour, IfcDefinedSymbol, IfcDefinedSymbolSelect, IfcDerivedMeasureValue, IfcDerivedProfileDef, IfcDerivedUnit, IfcDerivedUnitElement, IfcDerivedUnitEnum, IfcDescriptiveMeasure, IfcDiameterDimension, IfcDimensionCalloutRelationship, IfcDimensionCount, IfcDimensionCurve, IfcDimensionCurveDirectedCallout, IfcDimensionCurveTerminator, IfcDimensionExtentUsage, IfcDimensionPair, IfcDimensionalExponents, IfcDirection, IfcDirectionSenseEnum, IfcDiscreteAccessory, IfcDiscreteAccessoryType, IfcDistributionChamberElement, IfcDistributionChamberElementType, IfcDistributionChamberElementTypeEnum, IfcDistributionControlElement, IfcDistributionControlElementType, IfcDistributionElement, IfcDistributionElementType, IfcDistributionFlowElement, IfcDistributionFlowElementType, IfcDistributionPort, IfcDocumentConfidentialityEnum, IfcDocumentElectronicFormat, IfcDocumentInformation, IfcDocumentInformationRelationship, IfcDocumentReference, IfcDocumentSelect, IfcDocumentStatusEnum, IfcDoor, IfcDoorLiningProperties, IfcDoorPanelOperationEnum, IfcDoorPanelPositionEnum, IfcDoorPanelProperties, IfcDoorStyle, IfcDoorStyleConstructionEnum, IfcDoorStyleOperationEnum, IfcDoseEquivalentMeasure, IfcDraughtingCallout, IfcDraughtingCalloutElement, IfcDraughtingCalloutRelationship, IfcDraughtingPreDefinedColour, IfcDraughtingPreDefinedCurveFont, IfcDraughtingPreDefinedTextFont, IfcDuctFittingType, IfcDuctFittingTypeEnum, IfcDuctSegmentType, IfcDuctSegmentTypeEnum, IfcDuctSilencerType, IfcDuctSilencerTypeEnum, IfcDynamicViscosityMeasure, IfcEdge, IfcEdgeCurve, IfcEdgeFeature, IfcEdgeLoop, IfcElectricApplianceType, IfcElectricApplianceTypeEnum, IfcElectricCapacitanceMeasure, IfcElectricChargeMeasure, IfcElectricConductanceMeasure, IfcElectricCurrentEnum, IfcElectricCurrentMeasure, IfcElectricDistributionPoint, IfcElectricDistributionPointFunctionEnum, IfcElectricFlowStorageDeviceType, IfcElectricFlowStorageDeviceTypeEnum, IfcElectricGeneratorType, IfcElectricGeneratorTypeEnum, IfcElectricHeaterType, IfcElectricHeaterTypeEnum, IfcElectricMotorType, IfcElectricMotorTypeEnum, IfcElectricResistanceMeasure, IfcElectricTimeControlType, IfcElectricTimeControlTypeEnum, IfcElectricVoltageMeasure, IfcElectricalBaseProperties, IfcElectricalCircuit, IfcElectricalElement, IfcElement, IfcElementAssembly, IfcElementAssemblyTypeEnum, IfcElementComponent, IfcElementComponentType, IfcElementCompositionEnum, IfcElementQuantity, IfcElementType, IfcElementarySurface, IfcEllipse, IfcEllipseProfileDef, IfcEnergyConversionDevice, IfcEnergyConversionDeviceType, IfcEnergyMeasure, IfcEnergyProperties, IfcEnergySequenceEnum, IfcEnvironmentalImpactCategoryEnum, IfcEnvironmentalImpactValue, IfcEquipmentElement, IfcEquipmentStandard, IfcEvaporativeCoolerType, IfcEvaporativeCoolerTypeEnum, IfcEvaporatorType, IfcEvaporatorTypeEnum, IfcExtendedMaterialProperties, IfcExternalReference, IfcExternallyDefinedHatchStyle, IfcExternallyDefinedSurfaceStyle, IfcExternallyDefinedSymbol, IfcExternallyDefinedTextFont, IfcExtrudedAreaSolid, IfcFace, IfcFaceBasedSurfaceModel, IfcFaceBound, IfcFaceOuterBound, IfcFaceSurface, IfcFacetedBrep, IfcFacetedBrepWithVoids, IfcFailureConnectionCondition, IfcFanType, IfcFanTypeEnum, IfcFastener, IfcFastenerType, IfcFeatureElement, IfcFeatureElementAddition, IfcFeatureElementSubtraction, IfcFillAreaStyle, IfcFillAreaStyleHatching, IfcFillAreaStyleTileShapeSelect, IfcFillAreaStyleTileSymbolWithStyle, IfcFillAreaStyleTiles, IfcFillStyleSelect, IfcFilterType, IfcFilterTypeEnum, IfcFireSuppressionTerminalType, IfcFireSuppressionTerminalTypeEnum, IfcFlowController, IfcFlowControllerType, IfcFlowDirectionEnum, IfcFlowFitting, IfcFlowFittingType, IfcFlowInstrumentType, IfcFlowInstrumentTypeEnum, IfcFlowMeterType, IfcFlowMeterTypeEnum, IfcFlowMovingDevice, IfcFlowMovingDeviceType, IfcFlowSegment, IfcFlowSegmentType, IfcFlowStorageDevice, IfcFlowStorageDeviceType, IfcFlowTerminal, IfcFlowTerminalType, IfcFlowTreatmentDevice, IfcFlowTreatmentDeviceType, IfcFluidFlowProperties, IfcFontStyle, IfcFontVariant, IfcFontWeight, IfcFooting, IfcFootingTypeEnum, IfcForceMeasure, IfcFrequencyMeasure, IfcFuelProperties, IfcFurnishingElement, IfcFurnishingElementType, IfcFurnitureStandard, IfcFurnitureType, IfcGasTerminalType, IfcGasTerminalTypeEnum, IfcGeneralMaterialProperties, IfcGeneralProfileProperties, IfcGeometricCurveSet, IfcGeometricProjectionEnum, IfcGeometricRepresentationContext, IfcGeometricRepresentationItem, IfcGeometricRepresentationSubContext, IfcGeometricSet, IfcGeometricSetSelect, IfcGlobalOrLocalEnum, IfcGloballyUniqueId, IfcGrid, IfcGridAxis, IfcGridPlacement, IfcGroup, IfcHalfSpaceSolid, IfcHatchLineDistanceSelect, IfcHeatExchangerType, IfcHeatExchangerTypeEnum, IfcHeatFluxDensityMeasure, IfcHeatingValueMeasure, IfcHourInDay, IfcHumidifierType, IfcHumidifierTypeEnum, IfcHygroscopicMaterialProperties, IfcIShapeProfileDef, IfcIdentifier, IfcIlluminanceMeasure, IfcImageTexture, IfcInductanceMeasure, IfcInteger, IfcIntegerCountRateMeasure, IfcInternalOrExternalEnum, IfcInventory, IfcInventoryTypeEnum, IfcIonConcentrationMeasure, IfcIrregularTimeSeries, IfcIrregularTimeSeriesValue, IfcIsothermalMoistureCapacityMeasure, IfcJunctionBoxType, IfcJunctionBoxTypeEnum, IfcKinematicViscosityMeasure, IfcLShapeProfileDef, IfcLabel, IfcLaborResource, IfcLampType, IfcLampTypeEnum, IfcLayerSetDirectionEnum, IfcLayeredItem, IfcLengthMeasure, IfcLibraryInformation, IfcLibraryReference, IfcLibrarySelect, IfcLightDistributionCurveEnum, IfcLightDistributionData, IfcLightDistributionDataSourceSelect, IfcLightEmissionSourceEnum, IfcLightFixtureType, IfcLightFixtureTypeEnum, IfcLightIntensityDistribution, IfcLightSource, IfcLightSourceAmbient, IfcLightSourceDirectional, IfcLightSourceGoniometric, IfcLightSourcePositional, IfcLightSourceSpot, IfcLine, IfcLinearDimension, IfcLinearForceMeasure, IfcLinearMomentMeasure, IfcLinearStiffnessMeasure, IfcLinearVelocityMeasure, IfcLoadGroupTypeEnum, IfcLocalPlacement, IfcLocalTime, IfcLogical, IfcLogicalOperatorEnum, IfcLoop, IfcLuminousFluxMeasure, IfcLuminousIntensityDistributionMeasure, IfcLuminousIntensityMeasure, IfcMagneticFluxDensityMeasure, IfcMagneticFluxMeasure, IfcManifoldSolidBrep, IfcMappedItem, IfcMassDensityMeasure, IfcMassFlowRateMeasure, IfcMassMeasure, IfcMassPerLengthMeasure, IfcMaterial, IfcMaterialClassificationRelationship, IfcMaterialDefinitionRepresentation, IfcMaterialLayer, IfcMaterialLayerSet, IfcMaterialLayerSetUsage, IfcMaterialList, IfcMaterialProperties, IfcMaterialSelect, IfcMeasureValue, IfcMeasureWithUnit, IfcMechanicalConcreteMaterialProperties, IfcMechanicalFastener, IfcMechanicalFastenerType, IfcMechanicalMaterialProperties, IfcMechanicalSteelMaterialProperties, IfcMember, IfcMemberType, IfcMemberTypeEnum, IfcMetric, IfcMetricValueSelect, IfcMinuteInHour, IfcModulusOfElasticityMeasure, IfcModulusOfLinearSubgradeReactionMeasure, IfcModulusOfRotationalSubgradeReactionMeasure, IfcModulusOfSubgradeReactionMeasure, IfcMoistureDiffusivityMeasure, IfcMolecularWeightMeasure, IfcMomentOfInertiaMeasure, IfcMonetaryMeasure, IfcMonetaryUnit, IfcMonthInYearNumber, IfcMotorConnectionType, IfcMotorConnectionTypeEnum, IfcMove, IfcNamedUnit, IfcNormalisedRatioMeasure, IfcNullStyle, IfcNumericMeasure, IfcObject, IfcObjectDefinition, IfcObjectPlacement, IfcObjectReferenceSelect, IfcObjectTypeEnum, IfcObjective, IfcObjectiveEnum, IfcOccupant, IfcOccupantTypeEnum, IfcOffsetCurve2D, IfcOffsetCurve3D, IfcOneDirectionRepeatFactor, IfcOpenShell, IfcOpeningElement, IfcOpticalMaterialProperties, IfcOrderAction, IfcOrganization, IfcOrganizationRelationship, IfcOrientationSelect, IfcOrientedEdge, IfcOutletType, IfcOutletTypeEnum, IfcOwnerHistory, IfcPHMeasure, IfcParameterValue, IfcParameterizedProfileDef, IfcPath, IfcPerformanceHistory, IfcPermeableCoveringOperationEnum, IfcPermeableCoveringProperties, IfcPermit, IfcPerson, IfcPersonAndOrganization, IfcPhysicalComplexQuantity, IfcPhysicalOrVirtualEnum, IfcPhysicalQuantity, IfcPhysicalSimpleQuantity, IfcPile, IfcPileConstructionEnum, IfcPileTypeEnum, IfcPipeFittingType, IfcPipeFittingTypeEnum, IfcPipeSegmentType, IfcPipeSegmentTypeEnum, IfcPixelTexture, IfcPlacement, IfcPlanarBox, IfcPlanarExtent, IfcPlanarForceMeasure, IfcPlane, IfcPlaneAngleMeasure, IfcPlate, IfcPlateType, IfcPlateTypeEnum, IfcPoint, IfcPointOnCurve, IfcPointOnSurface, IfcPointOrVertexPoint, IfcPolyLoop, IfcPolygonalBoundedHalfSpace, IfcPolyline, IfcPort, IfcPositiveLengthMeasure, IfcPositivePlaneAngleMeasure, IfcPositiveRatioMeasure, IfcPostalAddress, IfcPowerMeasure, IfcPreDefinedColour, IfcPreDefinedCurveFont, IfcPreDefinedDimensionSymbol, IfcPreDefinedItem, IfcPreDefinedPointMarkerSymbol, IfcPreDefinedSymbol, IfcPreDefinedTerminatorSymbol, IfcPreDefinedTextFont, IfcPresentableText, IfcPresentationLayerAssignment, IfcPresentationLayerWithStyle, IfcPresentationStyle, IfcPresentationStyleAssignment, IfcPresentationStyleSelect, IfcPressureMeasure, IfcProcedure, IfcProcedureTypeEnum, IfcProcess, IfcProduct, IfcProductDefinitionShape, IfcProductRepresentation, IfcProductsOfCombustionProperties, IfcProfileDef, IfcProfileProperties, IfcProfileTypeEnum, IfcProject, IfcProjectOrder, IfcProjectOrderRecord, IfcProjectOrderRecordTypeEnum, IfcProjectOrderTypeEnum, IfcProjectedOrTrueLengthEnum, IfcProjectionCurve, IfcProjectionElement, IfcProperty, IfcPropertyBoundedValue, IfcPropertyConstraintRelationship, IfcPropertyDefinition, IfcPropertyDependencyRelationship, IfcPropertyEnumeratedValue, IfcPropertyEnumeration, IfcPropertyListValue, IfcPropertyReferenceValue, IfcPropertySet, IfcPropertySetDefinition, IfcPropertySingleValue, IfcPropertySourceEnum, IfcPropertyTableValue, IfcProtectiveDeviceType, IfcProtectiveDeviceTypeEnum, IfcProxy, IfcPumpType, IfcPumpTypeEnum, IfcQuantityArea, IfcQuantityCount, IfcQuantityLength, IfcQuantityTime, IfcQuantityVolume, IfcQuantityWeight, IfcRadioActivityMeasure, IfcRadiusDimension, IfcRailing, IfcRailingType, IfcRailingTypeEnum, IfcRamp, IfcRampFlight, IfcRampFlightType, IfcRampFlightTypeEnum, IfcRampTypeEnum, IfcRatioMeasure, IfcRationalBezierCurve, IfcReal, IfcRectangleHollowProfileDef, IfcRectangleProfileDef, IfcRectangularPyramid, IfcRectangularTrimmedSurface, IfcReferencesValueDocument, IfcReflectanceMethodEnum, IfcRegularTimeSeries, IfcReinforcementBarProperties, IfcReinforcementDefinitionProperties, IfcReinforcingBar, IfcReinforcingBarRoleEnum, IfcReinforcingBarSurfaceEnum, IfcReinforcingElement, IfcReinforcingMesh, IfcRelAggregates, IfcRelAssigns, IfcRelAssignsTasks, IfcRelAssignsToActor, IfcRelAssignsToControl, IfcRelAssignsToGroup, IfcRelAssignsToProcess, IfcRelAssignsToProduct, IfcRelAssignsToProjectOrder, IfcRelAssignsToResource, IfcRelAssociates, IfcRelAssociatesAppliedValue, IfcRelAssociatesApproval, IfcRelAssociatesClassification, IfcRelAssociatesConstraint, IfcRelAssociatesDocument, IfcRelAssociatesLibrary, IfcRelAssociatesMaterial, IfcRelAssociatesProfileProperties, IfcRelConnects, IfcRelConnectsElements, IfcRelConnectsPathElements, IfcRelConnectsPortToElement, IfcRelConnectsPorts, IfcRelConnectsStructuralActivity, IfcRelConnectsStructuralElement, IfcRelConnectsStructuralMember, IfcRelConnectsWithEccentricity, IfcRelConnectsWithRealizingElements, IfcRelContainedInSpatialStructure, IfcRelCoversBldgElements, IfcRelCoversSpaces, IfcRelDecomposes, IfcRelDefines, IfcRelDefinesByProperties, IfcRelDefinesByType, IfcRelFillsElement, IfcRelFlowControlElements, IfcRelInteractionRequirements, IfcRelNests, IfcRelOccupiesSpaces, IfcRelOverridesProperties, IfcRelProjectsElement, IfcRelReferencedInSpatialStructure, IfcRelSchedulesCostItems, IfcRelSequence, IfcRelServicesBuildings, IfcRelSpaceBoundary, IfcRelVoidsElement, IfcRelationship, IfcRelaxation, IfcRepresentation, IfcRepresentationContext, IfcRepresentationItem, IfcRepresentationMap, IfcResource, IfcResourceConsumptionEnum, IfcRevolvedAreaSolid, IfcRibPlateDirectionEnum, IfcRibPlateProfileProperties, IfcRightCircularCone, IfcRightCircularCylinder, IfcRoleEnum, IfcRoof, IfcRoofTypeEnum, IfcRoot, IfcRotationalFrequencyMeasure, IfcRotationalMassMeasure, IfcRotationalStiffnessMeasure, IfcRoundedEdgeFeature, IfcRoundedRectangleProfileDef, IfcSIPrefix, IfcSIUnit, IfcSIUnitName, IfcSanitaryTerminalType, IfcSanitaryTerminalTypeEnum, IfcScheduleTimeControl, IfcSecondInMinute, IfcSectionModulusMeasure, IfcSectionProperties, IfcSectionReinforcementProperties, IfcSectionTypeEnum, IfcSectionalAreaIntegralMeasure, IfcSectionedSpine, IfcSensorType, IfcSensorTypeEnum, IfcSequenceEnum, IfcServiceLife, IfcServiceLifeFactor, IfcServiceLifeFactorTypeEnum, IfcServiceLifeTypeEnum, IfcShapeAspect, IfcShapeModel, IfcShapeRepresentation, IfcShearModulusMeasure, IfcShell, IfcShellBasedSurfaceModel, IfcSimpleProperty, IfcSimpleValue, IfcSite, IfcSizeSelect, IfcSlab, IfcSlabType, IfcSlabTypeEnum, IfcSlippageConnectionCondition, IfcSolidAngleMeasure, IfcSolidModel, IfcSoundPowerMeasure, IfcSoundPressureMeasure, IfcSoundProperties, IfcSoundScaleEnum, IfcSoundValue, IfcSpace, IfcSpaceHeaterType, IfcSpaceHeaterTypeEnum, IfcSpaceProgram, IfcSpaceThermalLoadProperties, IfcSpaceType, IfcSpaceTypeEnum, IfcSpatialStructureElement, IfcSpatialStructureElementType, IfcSpecificHeatCapacityMeasure, IfcSpecularExponent, IfcSpecularHighlightSelect, IfcSpecularRoughness, IfcSphere, IfcStackTerminalType, IfcStackTerminalTypeEnum, IfcStair, IfcStairFlight, IfcStairFlightType, IfcStairFlightTypeEnum, IfcStairTypeEnum, IfcStateEnum, IfcStructuralAction, IfcStructuralActivity, IfcStructuralActivityAssignmentSelect, IfcStructuralAnalysisModel, IfcStructuralConnection, IfcStructuralConnectionCondition, IfcStructuralCurveConnection, IfcStructuralCurveMember, IfcStructuralCurveMemberVarying, IfcStructuralCurveTypeEnum, IfcStructuralItem, IfcStructuralLinearAction, IfcStructuralLinearActionVarying, IfcStructuralLoad, IfcStructuralLoadGroup, IfcStructuralLoadLinearForce, IfcStructuralLoadPlanarForce, IfcStructuralLoadSingleDisplacement, IfcStructuralLoadSingleDisplacementDistortion, IfcStructuralLoadSingleForce, IfcStructuralLoadSingleForceWarping, IfcStructuralLoadStatic, IfcStructuralLoadTemperature, IfcStructuralMember, IfcStructuralPlanarAction, IfcStructuralPlanarActionVarying, IfcStructuralPointAction, IfcStructuralPointConnection, IfcStructuralPointReaction, IfcStructuralProfileProperties, IfcStructuralReaction, IfcStructuralResultGroup, IfcStructuralSteelProfileProperties, IfcStructuralSurfaceConnection, IfcStructuralSurfaceMember, IfcStructuralSurfaceMemberVarying, IfcStructuralSurfaceTypeEnum, IfcStructuredDimensionCallout, IfcStyleModel, IfcStyledItem, IfcStyledRepresentation, IfcSubContractResource, IfcSubedge, IfcSurface, IfcSurfaceCurveSweptAreaSolid, IfcSurfaceOfLinearExtrusion, IfcSurfaceOfRevolution, IfcSurfaceOrFaceSurface, IfcSurfaceSide, IfcSurfaceStyle, IfcSurfaceStyleElementSelect, IfcSurfaceStyleLighting, IfcSurfaceStyleRefraction, IfcSurfaceStyleRendering, IfcSurfaceStyleShading, IfcSurfaceStyleWithTextures, IfcSurfaceTexture, IfcSurfaceTextureEnum, IfcSweptAreaSolid, IfcSweptDiskSolid, IfcSweptSurface, IfcSwitchingDeviceType, IfcSwitchingDeviceTypeEnum, IfcSymbolStyle, IfcSymbolStyleSelect, IfcSystem, IfcSystemFurnitureElementType, IfcTShapeProfileDef, IfcTable, IfcTableRow, IfcTankType, IfcTankTypeEnum, IfcTask, IfcTelecomAddress, IfcTemperatureGradientMeasure, IfcTendon, IfcTendonAnchor, IfcTendonTypeEnum, IfcTerminatorSymbol, IfcText, IfcTextAlignment, IfcTextDecoration, IfcTextFontName, IfcTextFontSelect, IfcTextLiteral, IfcTextLiteralWithExtent, IfcTextPath, IfcTextStyle, IfcTextStyleFontModel, IfcTextStyleForDefinedFont, IfcTextStyleSelect, IfcTextStyleTextModel, IfcTextStyleWithBoxCharacteristics, IfcTextTransformation, IfcTextureCoordinate, IfcTextureCoordinateGenerator, IfcTextureMap, IfcTextureVertex, IfcThermalAdmittanceMeasure, IfcThermalConductivityMeasure, IfcThermalExpansionCoefficientMeasure, IfcThermalLoadSourceEnum, IfcThermalLoadTypeEnum, IfcThermalMaterialProperties, IfcThermalResistanceMeasure, IfcThermalTransmittanceMeasure, IfcThermodynamicTemperatureMeasure, IfcTimeMeasure, IfcTimeSeries, IfcTimeSeriesDataTypeEnum, IfcTimeSeriesReferenceRelationship, IfcTimeSeriesSchedule, IfcTimeSeriesScheduleTypeEnum, IfcTimeSeriesValue, IfcTimeStamp, IfcTopologicalRepresentationItem, IfcTopologyRepresentation, IfcTorqueMeasure, IfcTransformerType, IfcTransformerTypeEnum, IfcTransitionCode, IfcTransportElement, IfcTransportElementType, IfcTransportElementTypeEnum, IfcTrapeziumProfileDef, IfcTrimmedCurve, IfcTrimmingPreference, IfcTrimmingSelect, IfcTubeBundleType, IfcTubeBundleTypeEnum, IfcTwoDirectionRepeatFactor, IfcTypeObject, IfcTypeProduct, IfcUShapeProfileDef, IfcUnit, IfcUnitAssignment, IfcUnitEnum, IfcUnitaryEquipmentType, IfcUnitaryEquipmentTypeEnum, IfcValue, IfcValveType, IfcValveTypeEnum, IfcVaporPermeabilityMeasure, IfcVector, IfcVectorOrDirection, IfcVertex, IfcVertexBasedTextureMap, IfcVertexLoop, IfcVertexPoint, IfcVibrationIsolatorType, IfcVibrationIsolatorTypeEnum, IfcVirtualElement, IfcVirtualGridIntersection, IfcVolumeMeasure, IfcVolumetricFlowRateMeasure, IfcWall, IfcWallStandardCase, IfcWallType, IfcWallTypeEnum, IfcWarpingConstantMeasure, IfcWarpingMomentMeasure, IfcWasteTerminalType, IfcWasteTerminalTypeEnum, IfcWaterProperties, IfcWindow, IfcWindowLiningProperties, IfcWindowPanelOperationEnum, IfcWindowPanelPositionEnum, IfcWindowPanelProperties, IfcWindowStyle, IfcWindowStyleConstructionEnum, IfcWindowStyleOperationEnum, IfcWorkControl, IfcWorkControlTypeEnum, IfcWorkPlan, IfcWorkSchedule, IfcYearNumber, IfcZShapeProfileDef, IfcZone, UNDEFINED
    } Enum;
    IfcParse_EXPORT Enum Parent(Enum v);
    IfcParse_EXPORT Enum FromString(const std::string& s);
    IfcParse_EXPORT std::string ToString(Enum v);
    IfcParse_EXPORT bool IsSimple(Enum v);
}

}

#endif
