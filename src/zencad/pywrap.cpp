/*#include <boost/python.hpp>
using namespace boost::python;
*/
#include <zencad/base.h>
#include <zencad/cache.h>
#include <zencad/topo.h>
#include <zencad/solid.h>
#include <zencad/wire.h>
#include <zencad/face.h>
#include <zencad/boolops.h>
#include <zencad/trans.h>
#include <zencad/stl.h>
#include <zencad/widget.h>

#include <zencad/math3.h>

#include <pybind11/pybind11.h>
#include <pybind11/operators.h>
namespace py = pybind11;

#define DEF_TRANSFORM_OPERATIONS(TYPE) 				\
.def("transform", &TYPE::transform)				\
.def("translate", &TYPE::translate)				\
.def("up", &TYPE::up)							\
.def("down", &TYPE::down)						\
.def("right", &TYPE::right)						\
.def("left", &TYPE::left)						\
.def("forw", &TYPE::forw)						\
.def("back", &TYPE::back)						\
.def("rotateX", &TYPE::rotateX)					\
.def("rotateY", &TYPE::rotateY)					\
.def("rotateZ", &TYPE::rotateZ)					\
.def("mirrorX", &TYPE::mirrorX)					\
.def("mirrorY", &TYPE::mirrorY)					\
.def("mirrorZ", &TYPE::mirrorZ)					\
.def("mirrorXY", &TYPE::mirrorXY)				\
.def("mirrorYZ", &TYPE::mirrorYZ)				\
.def("mirrorXZ", &TYPE::mirrorXZ)				

PYBIND11_MODULE(zenlib, m) {
	py::class_<ZenCadObject, std::shared_ptr<ZenCadObject>>(m, "ZenCadObject")
		.def("get_hash1", &ZenCadObject::get_hash1)
		.def("get_hash2", &ZenCadObject::get_hash2)
		.def("get_hash_base64", &ZenCadObject::get_hash_base64)		
	;
	py::class_<ZenShape, ZenCadObject, std::shared_ptr<ZenShape>>(m, "ZenShape")
		.def("dump", &ZenShape::dump_binary);

	py::class_<ZenVertex, ZenShape, std::shared_ptr<ZenVertex>>(m, "ZenVertex")
		DEF_TRANSFORM_OPERATIONS(ZenVertex)
		.def(py::init<double, double, double>())
	;

	///SOLIDS
	py::class_<ZenSolid, ZenShape, std::shared_ptr<ZenSolid>>(m, "ZenSolid")
		DEF_TRANSFORM_OPERATIONS(ZenSolid)
		.def(py::self + py::self)
		.def(py::self - py::self)
		.def(py::self ^ py::self)
	;
	m.def("solid_load", zen_load<ZenSolid>);

	py::class_<ZenBox, ZenSolid, std::shared_ptr<ZenBox>>(m, "solid_box")
		.def(py::init<double, double, double>())
		.def(py::init<double, double, double, py::kwargs>());


	py::class_<ZenSphere, ZenSolid, std::shared_ptr<ZenSphere>>(m, "solid_sphere")
		.def(py::init<double>());


	py::class_<ZenCylinder, ZenSolid, std::shared_ptr<ZenCylinder>>(m, "solid_cylinder")
		.def(py::init<double, double>());

	py::class_<ZenTorus, ZenSolid, std::shared_ptr<ZenTorus>>(m, "solid_torus")
		.def(py::init<double, double>());

	py::class_<ZenWedge, ZenSolid, std::shared_ptr<ZenWedge>>(m, "solid_wedge")
		.def(py::init<double, double, double, double>());
	
	py::class_<ZenLinearExtrude, ZenSolid, std::shared_ptr<ZenLinearExtrude>>(m, "solid_linear_extrude")
		.def(py::init<std::shared_ptr<ZenFace>, double>())
		.def(py::init<std::shared_ptr<ZenFace>, ZenVector3>());

	py::class_<ZenLoft, ZenSolid, std::shared_ptr<ZenLoft>>(m, "solid_loft")
		.def(py::init<py::list>());
	
	///EDGES
	py::class_<ZenEdge, ZenShape, std::shared_ptr<ZenEdge>>(m, "ZenEdge")
		DEF_TRANSFORM_OPERATIONS(ZenEdge)
		.def("face", &ZenEdge::make_face)
	;
	py::class_<ZenSegment, ZenEdge, std::shared_ptr<ZenSegment>>(m, "edge_segment")
		.def(py::init<ZenPoint3, ZenPoint3>());

	py::class_<ZenEdgeCircle, ZenEdge, std::shared_ptr<ZenEdgeCircle>>(m, "edge_circle")
		.def(py::init<double>());

	py::class_<ZenCircleArcByPoints, ZenEdge, std::shared_ptr<ZenCircleArcByPoints>>(m, "edge_circle_arc_by_points")
		.def(py::init<ZenPoint3, ZenPoint3, ZenPoint3>());

	///WIRES
	py::class_<ZenWire, ZenShape, std::shared_ptr<ZenWire>>(m, "ZenWire")
		DEF_TRANSFORM_OPERATIONS(ZenWire)
		.def("face", &ZenWire::make_face)
	;

	py::class_<ZenPolySegment, ZenWire, std::shared_ptr<ZenPolySegment>>(m, "wire_polysegment")
		.def(py::init<py::list>())
		.def(py::init<py::list, py::kwargs>());

	///FACE	
	py::class_<ZenFace, ZenShape, std::shared_ptr<ZenFace>>(m, "ZenFace")
		DEF_TRANSFORM_OPERATIONS(ZenFace)
		.def(py::self + py::self)
		.def(py::self - py::self)
		.def(py::self ^ py::self)
		.def("fillet", &ZenFace::fillet)
	;

	py::class_<ZenPolygon, ZenFace, std::shared_ptr<ZenPolygon>>(m, "face_polygon")
		.def(py::init<py::list>());

	py::class_<ZenFilletFace, ZenFace, std::shared_ptr<ZenFilletFace>>(m, "face_fillet")
		.def(py::init<std::shared_ptr<ZenFace>, int>());
		
	py::class_<ZenCircle, ZenFace, std::shared_ptr<ZenCircle>>(m, "face_circle")
		.def(py::init<double>());

	///TRANS
	py::class_<ZenTransform, std::shared_ptr<ZenTransform>>(m, "ZenTransform");
	m.def("trans_translate", trans_translate);

	///COMPAT
	m.def("make_stl", make_stl);

	///CACHE
	m.def("cache_enable", zencache_enable);
	m.def("cache_disable", zencache_disable);
	m.def("cache_is_enabled", zencache_is_enabled);

	///VIEW
	m.def("display", display);
	m.def("show", show);

	py::class_<ZenDirection3>(m, "direction3").def(py::init<double,double,double>());
	py::class_<ZenVector3>(m, "vector3").def(py::init<double,double,double>());
	py::class_<ZenPoint3>(m, "point3")
		.def(py::init<double,double,double>())
		.def(py::init<double,double>());
		
}