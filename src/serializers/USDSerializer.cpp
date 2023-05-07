#ifdef WITH_USD

#include "USDSerializer.h"

#include "pxr/base/tf/token.h"
#include "pxr/base/gf/vec3f.h"
#include "pxr/base/gf/rotation.h"
#include "pxr/usd/usdGeom/xform.h"
#include "pxr/usd/usdGeom/xformOp.h"
#include "pxr/usd/usdGeom/tokens.h"
#include "pxr/usd/usdGeom/scope.h"
#include "pxr/usd/usdLux/distantLight.h"
#include "pxr/usd/usdShade/shader.h"
#include "pxr/usd/usdShade/tokens.h"
#include "pxr/usd/usdShade/materialBindingAPI.h"
#include "pxr/usd/usdShade/connectableAPI.h"

USDSerializer::USDSerializer(const std::string& out_filename, const SerializerSettings& settings):
  WriteOnlyGeometrySerializer(settings),
  filename_(out_filename)
{
  // create a new stage
  stage_ = pxr::UsdStage::CreateNew(filename_ + ".usda");

  pxr::UsdGeomXform::Define(stage_, pxr::SdfPath("/World"));
  pxr::UsdGeomScope::Define(stage_, pxr::SdfPath("/Looks"));
  createLighting();
  ready_ = true;
}

USDSerializer::~USDSerializer() {
	
}

void USDSerializer::createLighting() {
  // create a distant light
  const std::string& light_path = "/World/defaultLight";
  pxr::UsdLuxDistantLight::Define(stage_, pxr::SdfPath(light_path));
  // set the light's orientation
  pxr::UsdGeomXform xform(stage_->GetPrimAtPath(pxr::SdfPath(light_path)));
  pxr::GfVec3f light_direction(0.0f, 0.0f, -1.0f);
  //xform.AddRotateOp(pxr::UsdGeomXformOp::PrecisionFloat, pxr::UsdGeomXformOp::TypeRotateXYZ).Set(pxr::GfRotation(pxr::GfVec3f(0.0f, 1.0f, 0.0f), light_direction).GetQuaternion());
  // set the light's color
  pxr::UsdLuxDistantLight light(stage_->GetPrimAtPath(pxr::SdfPath(light_path)));
  light.CreateIntensityAttr().Set(1000.0f);
  light.CreateColorAttr().Set(pxr::GfVec3f(1.0f, 1.0f, 1.0f));
}

void USDSerializer::writeMaterial(const pxr::UsdGeomMesh& mesh,const IfcGeom::Material& style) {
  std::string path("/Looks/" + sanitize(style.original_name()));
  auto material = pxr::UsdShadeMaterial::Define(stage_, pxr::SdfPath(path));
  auto shader = pxr::UsdShadeShader::Define(stage_, pxr::SdfPath(path + "/Shader"));
  shader.CreateIdAttr().Set(pxr::TfToken("UsdPreviewSurface"));

  float rgba[4] { 0.18f, 0.18f, 0.18f, 1.0f };
  if (style.hasDiffuse())
		for (int i = 0; i < 3; ++i)
      rgba[i] = static_cast<float>(style.diffuse()[i]);
  shader.CreateInput(pxr::TfToken("diffuseColor"), pxr::SdfValueTypeNames->Color3f).Set(pxr::GfVec3f(rgba[0], rgba[1], rgba[2]));

  if(style.hasTransparency())
    rgba[3] -= style.transparency();
  shader.CreateInput(pxr::TfToken("opacity"), pxr::SdfValueTypeNames->Float).Set(rgba[3]);

  if(style.hasSpecular()) {
    for (int i = 0; i < 3; ++i)
      rgba[i] = static_cast<float>(style.specular()[i]);
    shader.CreateInput(pxr::TfToken("useSpecularWorkflow"), pxr::SdfValueTypeNames->Int).Set(1);
  } else {
    shader.CreateInput(pxr::TfToken("useSpecularWorkflow"), pxr::SdfValueTypeNames->Int).Set(0);
  }
  shader.CreateInput(pxr::TfToken("specularColor"), pxr::SdfValueTypeNames->Color3f).Set(pxr::GfVec3f(rgba[0], rgba[1], rgba[2]));

  material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), pxr::TfToken("surface"));
  pxr::UsdShadeMaterialBindingAPI(mesh).Bind(material);
}

bool USDSerializer::ready() {
	return ready_;
}

void USDSerializer::writeHeader() {
  stage_->GetRootLayer()->SetComment("File generated by IfcOpenShell " + std::string(IFCOPENSHELL_VERSION)); 
}

void USDSerializer::write(const IfcGeom::TriangulationElement* o) {
  const IfcGeom::Representation::Triangulation& mesh = o->geometry();
  auto verts = mesh.verts();
  auto faces = mesh.faces();
  const std::vector<double>& m = o->transformation().matrix().data();

	if ( mesh.material_ids().empty() || verts.empty() || faces.empty() )
		return;
  
  std::string name = o->name() + std::to_string(o->id());
  if(name.empty()) {
    name = "Unnamed_" + std::to_string(unnamed_count_);
    unnamed_count_++;
  } else {
    name = sanitize(name);
  }
  pxr::UsdGeomMesh usd_mesh = pxr::UsdGeomMesh::Define(stage_, pxr::SdfPath("/World/" + name));

  usd_mesh.AddTranslateOp().Set(pxr::GfVec3d(m[9], m[10], m[11]));

  pxr::VtVec3fArray points;
  for(std::size_t i = 0; i < verts.size(); i+=3) {
    points.push_back(pxr::GfVec3f(static_cast<float>(verts[i] * m[0] + verts[i+1] * m[3] + verts[i+2] * m[6]),
                                  static_cast<float>(verts[i] * m[1] + verts[i+1] * m[4] + verts[i+2] * m[7]),
                                  static_cast<float>(verts[i] * m[2] + verts[i+1] * m[5] + verts[i+2] * m[8])));
  }
  usd_mesh.CreatePointsAttr().Set(points);

  usd_mesh.CreateFaceVertexIndicesAttr().Set(usd_utils::toVtArray(faces));
  usd_mesh.CreateFaceVertexCountsAttr().Set(pxr::VtArray<int>((int) faces.size() / 3, 3));

  pxr::VtVec3fArray normals;
  for (std::vector<double>::const_iterator it = mesh.normals().begin(); it != mesh.normals().end();)
    normals.push_back(pxr::GfVec3f(static_cast<float>(*(it++)), static_cast<float>(*(it++)), static_cast<float>(*(it++))));
  usd_mesh.CreateNormalsAttr().Set(normals);

  writeMaterial(usd_mesh, mesh.materials()[0]);
}

void USDSerializer::finalize() {
  stage_->Save();
}

#endif // WITH_USD